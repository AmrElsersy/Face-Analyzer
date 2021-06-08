# import required library for GUI
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QPalette, QColor

# import matplotlib backend and figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.animation import TimedAnimation
from matplotlib.ticker import MaxNLocator

from utils import processData, dataSend

import matplotlib
import numpy as np
import threading

matplotlib.use("Qt5Agg")

class Live_Histogram(QWidget):
    def __init__(self):
        # call the constructor of the parent (QWidget)
        super(Live_Histogram, self).__init__()

        # # give orange background to the window
        # palette = self.palette()
        # palette.setColor(QPalette.Window,QColor(0, 128, 128))
        # self.setPalette(palette)
        # self.setAutoFillBackground(True)

        # setup the grid layout design and components
        self.customFig = CustomFigHist()
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.customFig)
        self.setLayout(self.vbox)

        dataLoop = threading.Thread(name='dataLoop', target=dataSend, daemon=True,
                                    args=(self.addData_callbackFunc,))
        dataLoop.start()

    def addData_callbackFunc(self, data):
        self.customFig.addData(data)


class CustomFigHist(FigureCanvas, TimedAnimation):
    def __init__(self):
        self.features = ['angry', 'disgust', 'fear', 'happy',
                         'sad', 'surprise', 'neutral', 'focus']

        self.current_features = [0] * 8
        self.steps = 0

        self.fig = Figure(figsize=(11, 9), dpi=100, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        self.ax = self.fig.add_subplot(111)
        self.patches = self.ax.bar(self.features, self.current_features,
                                   facecolor='green', edgecolor='yellow', alpha=0.5)
        self.ax.set_xlabel('Status')
        self.ax.set_ylabel('N')
        self.ax.set_title("Live Histogram")
        self.ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        self.ax.set_ylim(0, 1)

        FigureCanvas.__init__(self, self.fig)
        TimedAnimation.__init__(self, self.fig, interval=1000, blit=False, repeat=True)

    def new_frame_seq(self):
        it = iter(range(self.steps))
        return it

    def addData(self, data):
        status = processData(data)
        self.steps += 1

        for i in range(len(self.current_features)):
            self.current_features[i] = status[self.features[i]]

    def _step(self, *args):
        # extends the _step() method for the TimedAnimation class
        try:
            TimedAnimation._step(self, *args)
        except:
            TimedAnimation._stop(self)

    def _draw_frame(self, framedata):
        ylim_max = np.maximum.reduce(self.current_features).max() + 25
        ylim_min = np.minimum.reduce(self.current_features).min() - 25
        self.ax.set_ylim(ylim_min, ylim_max)

        for rect, h in zip(self.patches, self.current_features):
            rect.set_height(h)