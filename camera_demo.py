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

        video = None
        isOpened = False
        if not self.args.image:
            if self.args.path:
                video = cv2.VideoCapture(self.args.path)
            else:
                video = cv2.VideoCapture(0) # 480, 640
            isOpened = video.isOpened()
            print('video.isOpened:', isOpened)

        t1 = 0
        t2 = 0
        min_time = 1 / self.args.fps
        last_frame_time = 0


        if self.args.image:
            frame = cv2.imread(self.args.path)
        else:
            _, frame = video.read()
            isOpened = video.isOpened()

        # if loaded video or image (not live camera) .. resize it (helpful in mobile camera with has different resolution)
        if self.args.path:
            frame = cv2.resize(frame, (640, 480))

        # time
        t2 = time.time()
        fps = round(1/(t2-t1))
        t1 = t2

        # check min time
        if (t2 - last_frame_time) >= min_time:
            # reset timing calculations
            last_frame_time = t2

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

                status["time"] = str(int(time.time()/(max(min_time * 0.9, 1e-4))))

                # send to the server
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
                    'time': str(int(time.time() / (max(min_time * 0.9, 1e-4))))
                }
                # print(info)
                requests.post(self.args.url, json=info)

                # cv2.imshow('input face', cv2.resize(input_face, (120, 120)))
                # cv2.rectangle(frame, (x, y), (x + w, y + h), (200, 100, 0), 3)
                # cv2.putText(
                #     frame,
                #     focus,
                #     (x, y + 1),
                #     cv2.FONT_HERSHEY_SIMPLEX,
                #     0.8,
                #     (0, 200, 200),
                #     2,
                # )
                # cv2.putText(
                #     frame,
                #     "{} {}".format(emotion_label, int(emotion_prob * 100)),
                #     (x+w, y + 1),
                #     cv2.FONT_HERSHEY_SIMPLEX,
                #     0.8,
                #     (0, 200, 200),
                #     2,
                # )

            # draw FPS
            # cv2.putText(frame, str(fps), (10,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0))
            # cv2.imshow("Video", frame)
            # if cv2.waitKey(1) & 0xff == 27:
            #     if not args.image:
            #         video.release()
            #     break

            if not self.args.image:
                video.release()