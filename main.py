from PyQt5.QtWidgets import QApplication
from software.main_widget import Live_Statistics
from camera_demo import analyze_face
from easydict import EasyDict as edict
from software.utils import Thread
import argparse
import requests
import sys


def parse_configs():
    parser = argparse.ArgumentParser(description='Face Analyzer')
    parser.add_argument('--type', type=str, default="student", help="run meeting application")
    parser.add_argument('--url', type=str, default='https://airay2-backend.herokuapp.com/faces_info')
    parser.add_argument('--name', type=str, help='unique name of the user', default='ray2')
    parser.add_argument('--haar', action='store_true', help='run the haar cascade face detector')
    parser.add_argument('--path', type=str, default='', help='path to video to test')
    parser.add_argument('--image', action='store_true', help='specify if you test image or not')
    parser.add_argument('--fps', type=int, default=0.1, help='num of frames per second to capture info')
    configs = edict(vars(parser.parse_args()))

    return configs

def data_send(cfg, signal):
    data = requests.get(cfg.url)
    signal.thread_signal.emit(data)

def main():
    app = QApplication(sys.argv)
    cfg = parse_configs()
    user_type = cfg.type
    live = None
    signal = None
    if user_type == "doctor":
        live = Live_Statistics()
        signal = Thread()
        signal.thread_signal.connect(live.addData_callbackFunc)
        live.show()
        sys.exit(app.exec_())

    while True:
        analyze_face(cfg)
        if user_type == "doctor":
            data_send(cfg, signal)


if __name__ == "__main__":
    main()