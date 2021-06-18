from flask import Flask, request, jsonify
from threading import Thread, Event
import socket, json
import pickle
import collections
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
        self.faces_infos = dict()
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.target_address = None
        self.current= collections.deque([])

    def add_info(self, face_info):
        flag = True
        if not face_info['time'] in self.faces_infos:
            if len(self.current) == 2: #You can change the length here, according how long the you are okay with the delaying
                pickle_msg = pickle.dumps(self.faces_infos[self.current[0]])#send this to the application
                self.socket.sendto(pickle_msg, self.target_address)
                del self.faces_infos[self.current[0]]
                self.current.popleft()
            self.faces_infos.setdefault(face_info['time'], []).append(face_info['data'])
            self.current.append(face_info['time'])
        for info in self.faces_infos[face_info['time']]:
            if info['name'] == face_info['data']['name']:
                flag = False
                break
        if flag:
            self.faces_infos.setdefault(face_info['time'], []).append(face_info['data'])

#  ===================== App - Tracker ========================
app = Flask(__name__)
tracker = FaceInfoTracker()

# ======================== Timer Thread ========================
# class MyThread(Thread):
#     def __init__(self, wait_time):
#         Thread.__init__(self)
#         self.stopped = Event()
#         self.wait_time = wait_time

#     def run(self):
#         while not self.stopped.wait(self.wait_time):
#             tracker.clear()

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

    # thread = MyThread(2)
    # thread.start()

    ip = "127.0.0.1"
    port = 8008

    app.run(host=ip, port=port)

