from math import floor
import sys
import time
import cv2
import torch
from face_detector.face_detector import DnnDetector, HaarCascadeDetector
from utils import normalization, histogram_equalization, standerlization
from face_alignment.face_alignment import FaceAlignment
from emotion_recognizer.emotion_recognition import recognize_face
from gaze_tracking.focusDetection import focusDetector
import requests

sys.path.insert(1, 'face_detector')
sys.path.insert(2, 'GazeTracking')
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Face_Analyzer:
    def __init__(self, args):
        self.args = args
        self.face_alignment = FaceAlignment()
        self.focus_detector = focusDetector()

        if not self.args.image:
            if self.args.path:
                self.video = cv2.VideoCapture(self.args.path)
            else:
                self.video = cv2.VideoCapture(0) # 480, 640
            isOpened = self.video.isOpened()
            print('video.isOpened:', isOpened)

        # Face detection
        root = 'face_detector'
        self.face_detector = None
        if self.args.haar:
            self.face_detector = HaarCascadeDetector(root)
        else:
            self.face_detector = DnnDetector(root)

    def get_emotion(self, face):
        return recognize_face(face)

    def hisEqulColor(self, img):
        ycrcb=cv2.cvtColor(img,cv2.COLOR_BGR2YCR_CB)
        channels=cv2.split(ycrcb)
        cv2.equalizeHist(channels[0],channels[0])
        cv2.merge(channels,ycrcb)
        cv2.cvtColor(ycrcb,cv2.COLOR_YCR_CB2BGR,img)
        return img


    def analyze_face(self):
        status = {"angry": 0,
                  "disgust": 0,
                  "fear": 0,
                  "happy": 0,
                  "sad": 0,
                  "surprise": 0,
                  "neutral": 0,
                  "focus": 0,
                  "not focus": 0}

        t1 = 0
        t2 = 0
        # min_time = 1 / self.args.fps
        # last_frame_time = 0


        if self.args.image:
            frame = cv2.imread(self.args.path)
        else:
            _, frame = self.video.read()
            isOpened = self.video.isOpened()

        # if loaded video or image (not live camera) .. resize it (helpful in mobile camera with has different resolution)
        if self.args.path:
            frame = cv2.resize(frame, (640, 480))

        # # time
        # t2 = time.time()
        # fps = round(1/(t2-t1))
        # t1 = t2

        # check min time

        # faces
        faces = self.face_detector.detect_faces(frame)

        for face in faces:
            (x,y,w,h) = face

            # preprocessing
            input_face = self.face_alignment.frontalize_face(face, frame)

            emo_proba, emo_label = self.get_emotion(input_face)

            focus = self.focus_detector.focused(input_face)

            status[emo_label] = 1
            if focus:
                status["focus"] = 1
            else:
                status["not focus"] = 1

            info = {
                'data': {'name': self.args.name,
                         "angry": status["angry"],
                         "disgust": status["disgust"],
                         "fear": status["fear"],
                         "happy": status["happy"],
                         "sad": status["sad"],
                         "surprise": status["surprise"],
                         "neutral": status["neutral"],
                         "focus": status["focus"],
                         "not focus": status["not focus"]},
                'time': str(int(time.time() / (max((self.args.interval/1000), 1e-4))))
            }
            requests.post(self.args.url, json=info)

        # if not self.args.image:
        #     self.video.release()