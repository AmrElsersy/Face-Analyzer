from PyQt5.QtWidgets import QApplication
from main_widget import Live_Statistics
from easydict import EasyDict as edict
import argparse
import sys

def start_analyzer():
    main = Live_Statistics()
    main.show()

def parse_configs():
    parser = argparse.ArgumentParser(description='Face Analyzer')
    parser.add_argument('--type', type=str, default="student", help="run meeting application")
    configs = edict(vars(parser.parse_args()))

    return configs

def main():
    app = QApplication(sys.argv)
    cfg = parse_configs()
    user_type = cfg.type

    start_analyzer()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()