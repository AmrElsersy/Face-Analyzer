from PyQt5.QtWidgets import QApplication
from software.main_widget import Live_Statistics
from easydict import EasyDict as edict
import argparse
import requests
import sys


def parse_configs():
    parser = argparse.ArgumentParser(description='Face Analyzer')
    parser.add_argument('--type', type=str, default="doctor", help="run meeting application")
    parser.add_argument('--analyze_doctor', action='store_true', default=True, help="analyze face of doctor")
    parser.add_argument('--url', type=str, default='https://airay2-backend.herokuapp.com/faces_info')
    parser.add_argument('--name', type=str, help='unique name of the user', default='moamen')
    parser.add_argument('--interval', type=int, help='time interval for updating the graph', default=3000)
    parser.add_argument('--haar', action='store_true', help='run the haar cascade face detector')
    parser.add_argument('--path', type=str, default='', help='path to video to test')
    parser.add_argument('--image', action='store_true', help='specify if you test image or not')
    # parser.add_argument('--fps', type=int, default=0.25, help='num of frames per second to capture info')
    configs = edict(vars(parser.parse_args()))

    return configs

def main():
    app = QApplication(sys.argv)
    cfg = parse_configs()
    res = requests.get(cfg.url, "clear")
    user_type = cfg.type
    live = Live_Statistics(cfg)
    if user_type == "doctor":
        live.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()