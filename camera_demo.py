import sys
import time
import argparse
import cv2
import torch
from face_detector.face_detector import DnnDetector, HaarCascadeDetector
from utils import normalization, histogram_equalization, standerlization
from face_alignment.face_alignment import FaceAlignment
# from emotion_recognizer.emotion_recognition import recognize_face
from gaze_tracking.focusDetection import focusDetector
import requests

sys.path.insert(1, 'face_detector')
sys.path.insert(2, 'GazeTracking')
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def get_emotion(face):
    return 'not ray2'
    # return recognize_face(face)

def hisEqulColor(img):
    ycrcb=cv2.cvtColor(img,cv2.COLOR_BGR2YCR_CB)
    channels=cv2.split(ycrcb)
    cv2.equalizeHist(channels[0],channels[0])
    cv2.merge(channels,ycrcb)
    cv2.cvtColor(ycrcb,cv2.COLOR_YCR_CB2BGR,img)
    return img


def main(args):
    face_alignment = FaceAlignment()
    focus_detector = focusDetector()

    # Face detection
    root = 'face_detector'
    face_detector = None
    if args.haar:
        face_detector = HaarCascadeDetector(root)
    else:
        face_detector = DnnDetector(root)

    video = None
    isOpened = False
    if not args.image:
        if args.path:
            video = cv2.VideoCapture(args.path)
        else:
            video = cv2.VideoCapture(0) # 480, 640
        isOpened = video.isOpened()
        print('video.isOpened:', isOpened)

    t1 = 0
    t2 = 0
    min_time = 1 / args.fps
    last_frame_time = 0

    while args.image or isOpened:
        if args.image:
            frame = cv2.imread(args.path)
        else:
            _, frame = video.read()
            isOpened = video.isOpened()
        # if loaded video or image (not live camera) .. resize it (helpful in mobile camera with has different resolution)
        if args.path:
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
            faces = face_detector.detect_faces(frame)

            for face in faces:
                (x,y,w,h) = face

                # preprocessing
                input_face = face_alignment.frontalize_face(face, frame)

                emotion_label = get_emotion(input_face)
                # emotion_prob, emotion_label = get_emotion(input_face)

                focus = focus_detector.focused(input_face)

                info = {
                    'name': args.name,
                    'emotion': emotion_label,
                    'focus': focus
                }

                # send to the server
                requests.post(args.url, json=info)

                cv2.imshow('input face', cv2.resize(input_face, (120, 120)))
                cv2.rectangle(frame, (x, y), (x + w, y + h), (200, 100, 0), 3)
                cv2.putText(
                    frame,
                    focus,
                    (x, y + 1),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 200, 200),
                    2,
                )
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
        cv2.putText(frame, str(fps), (10,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0))
        cv2.imshow("Video", frame)
        if cv2.waitKey(1) & 0xff == 27:
            if not args.image:
                video.release()
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, default='http://127.0.0.1:8008/faces_info')
    parser.add_argument('--name', type=str, help='unique name of the user', default='ray2')
    parser.add_argument('--haar', action='store_true', help='run the haar cascade face detector')
    parser.add_argument('--path', type=str, default='', help='path to video to test')
    parser.add_argument('--image', action='store_true', help='specify if you test image or not')
    parser.add_argument('--fps', type=int, default=2, help='num of frames per second to capture info')
    args = parser.parse_args()

    main(args)

