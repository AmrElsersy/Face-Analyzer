from PyQt5.QtWidgets import QApplication
from software.main_widget import Live_Statistics
from camera_demo import Face_Analyzer
from easydict import EasyDict as edict
from software.utils import Thread, data_send
import argparse
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


def main():
    app = QApplication(sys.argv)
    cfg = parse_configs()
    analyzer = Face_Analyzer(cfg)
    user_type = cfg.type
    live = None
    signal = None
    if user_type == "doctor":
        live = Live_Statistics(cfg.url)
        signal = Thread()
        signal.thread_signal.connect(live.addData_callbackFunc)
        live.show()

    while True:
        analyzer.analyze_face()
        if user_type == "doctor":
            data_send(cfg.url, signal)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()