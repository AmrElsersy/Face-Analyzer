from flask import Flask, request, jsonify
import time
from threading import Thread, Timer, Event

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
        self.prev_faces_infos = []

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
        self.prev_faces_infos = self.faces_infos
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
            print("clear")
            tracker.clear()

# ======================== Routes ========================
@app.route("/faces_info",methods=["POST"])
def add_face_info():
    face_info = request.get_json()

    print("Added ", face_info)

    tracker.add_info(face_info)

    return jsonify ({
        "success":True
    }), 200

@app.route("/faces_info", methods=["GET"])
def get_faces_infos():

    # if the list is empty so it might be because the request time cames after the clear time
    # so set it to the prev faces info of the prev time
    if len(tracker.faces_infos) > 0:
        faces_infos = tracker.faces_infos
    else:
        faces_infos = tracker.prev_faces_infos

    return jsonify({
        "success" : True,
        "faces_infos" : faces_infos
    }), 200

if __name__ == '__main__':

    thread = MyThread(10)
    thread.start()

    ip = "127.0.0.1"
    port = 8008

    app.run(host=ip, port=port)

