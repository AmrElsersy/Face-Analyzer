from flask import Flask, request, jsonify
from threading import Thread, Event
import socket, json
import pickle

"""
Received Face Info
{
    "name": "NAME",
    "emotion": "happy",
    "focus": True
}
"""

class FaceInfoTracker:
    def __init__(self):
        # list of json faces infos
        self.faces_infos = []

        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.target_address = None

    def add_info(self, face_info):

        # if the same person sent a face info during the timeout, update its values
        update_old_info = False
        for info in self.faces_infos:
            if info['name'] == face_info['name']:
                info['emotion'] = face_info['emotion']
                info['focus'] = face_info['emotion']
                update_old_info = True
                break

        # if the face info dosn't exist in the faces list, add it
        if not update_old_info:
            self.faces_infos.append(face_info)

    def clear(self):
        print(self.faces_infos)

        if self.target_address:
            # send to ogranizer
            # encode with pickle .. converts the list into bytes
            pickle_msg = pickle.dumps(self.faces_infos)
            # send to udp receiver
            self.socket.sendto(pickle_msg, self.target_address)

        print("clear")
        self.faces_infos.clear()

#  ===================== App - Tracker ========================
app = Flask(__name__)
tracker = FaceInfoTracker()

# ======================== Timer Thread ========================
class MyThread(Thread):
    def __init__(self, wait_time):
        Thread.__init__(self)
        self.stopped = Event()
        self.wait_time = wait_time

    def run(self):
        while not self.stopped.wait(self.wait_time):
            tracker.clear()

# ======================== Routes ========================
# add face info .. should post json that contains "name" & "emotion" & "focus"
@app.route("/faces_info",methods=["POST"])
def add_face_info():
    face_info = request.get_json()

    print("Added ", face_info)

    tracker.add_info(face_info)

    return jsonify ({
        "success":True
    }), 200

# get all the faces info at this moment
@app.route("/faces_info", methods=["GET"])
def get_faces_infos():

    faces_infos = tracker.faces_infos
    return jsonify({
        "success" : True,
        "faces_infos" : faces_infos
    }), 200

# Set the target(organizer) ip & port which the server will send the faces_info data periodically
@app.route("/target_connection", methods=["POST"])
def set_target_address():
    address = request.get_json()
    ip = address['ip']
    port = address['port']

    tracker.target_address = (ip, port)
    print("set target ", address)

    return jsonify({
        "success": True,
        "target ip": ip,
        "target port": port
    }), 200

if __name__ == '__main__':

    thread = MyThread(4)
    thread.start()

    ip = "127.0.0.1"
    port = 8008

    app.run(host=ip, port=port)

