# import required library for GUI
from PyQt5.QtWidgets import QApplication,QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QCheckBox
from PyQt5.QtGui import QIcon, QPalette, QColor, QFont
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import QtGui

# import matplotlib backend and figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.animation import TimedAnimation
from matplotlib.ticker import MaxNLocator

from utils import processData

import matplotlib
import numpy as np
import sys
import os
import functools
import time
import threading

matplotlib.use("Qt5Agg")

class Live_Graph(QWidget):
    def __init__(self):
        # call the constructor of the parent (QWidget)
        super(Live_Graph, self).__init__()

        self.features = [('angry', '#1f77b4'),
                         ('disgust', '#ff7f0e'),
                         ('fear', '#2ca02c'),
                         ('happy', '#d62728'),
                         ('sad', '#9467bd'),
                         ('surprise', '#8c564b'),
                         ('neutral', '#e377c2'),
                         ('focus', '#7f7f7f')]
        self.angry = []
        self.disgust = []
        self.fear = []
        self.happy = []
        self.sad = []
        self.surprise = []
        self.neutral = []
        self.focus = []
        self.time = 0

        # set title  and geometry for the window
        self.setWindowTitle("Live Statistics")
        self.setGeometry(500,400,600,400)

        # give orange background to the window
        palette = self.palette()
        palette.setColor(QPalette.Window,QColor(150,150,150))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # set minimum width and height for the window
        self.setMinimumHeight(400)
        self.setMinimumWidth(600)
        self.setMaximumHeight(400)
        self.setMaximumWidth(600)

        # set icon for the application at run time and center the application window with the primary screen
        self.setIcon()
        self.center()

        # setup the grid layout design and components
        self.createPlotLayout()
        self.createCheckboxes()
        self.hbox = QHBoxLayout()
        self.hbox.addLayout(self.vbox_graph)
        self.hbox.addWidget(self.groupBox)
        self.setLayout(self.hbox)

        dataLoop = threading.Thread(name='dataLoop', target=dataSend, daemon=True,
                                      args=(self.addData_callbackFunc,))
        dataLoop.start()

    def addData_callbackFunc(self, data):
        self.customFig.addData(data)

    # set icon for the application
    def setIcon(self):
        appIcon = QIcon("icon.png")
        self.setWindowIcon(appIcon)

    # to center the application window at the beginning
    def center(self):
        qRect = self.frameGeometry()
        centerPoint = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qRect.moveCenter(centerPoint)
        self.move(qRect.topLeft())

    def createCheckboxes(self):
        # make group box with headline then add the gridlayout to it
        self.groupBox = QGroupBox("Status")
        self.groupBox.setFont(QFont("Helvetica", 12))

        # initialize checkboxes
        self.angry_cb = QCheckBox("Angry")
        self.angry_cb.setChecked(True)

        self.disgust_cb = QCheckBox("Disgust")
        self.disgust_cb.setChecked(True)

        self.fear_cb = QCheckBox("Fear")
        self.fear_cb.setChecked(True)

        self.happy_cb = QCheckBox("Happy")
        self.happy_cb.setChecked(True)

        self.sad_cb= QCheckBox("Sad")
        self.sad_cb.setChecked(True)

        self.surprise_cb = QCheckBox("Surprise")
        self.surprise_cb.setChecked(True)

        self.neutral_cb = QCheckBox("Neutral")
        self.neutral_cb.setChecked(True)

        self.focus_cb = QCheckBox("Focus")
        self.focus_cb.setChecked(True)

        # setup the grid layout design and components
        self.vbox_checkboxes = QVBoxLayout()
        self.vbox_checkboxes.addWidget(self.angry_cb)
        self.vbox_checkboxes.addWidget(self.disgust_cb)
        self.vbox_checkboxes.addWidget(self.fear_cb)
        self.vbox_checkboxes.addWidget(self.happy_cb)
        self.vbox_checkboxes.addWidget(self.sad_cb)
        self.vbox_checkboxes.addWidget(self.surprise_cb)
        self.vbox_checkboxes.addWidget(self.neutral_cb)
        self.vbox_checkboxes.addWidget(self.focus_cb)

        self.groupBox.setLayout(self.vbox_checkboxes)

    def createPlotLayout(self):
        # set the figure and toolbar and add it to the window
        # self.fig = Figure(figsize=(9, 7), dpi=65, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        # self.canvas = FigureCanvas(self.fig)
        # self.toolbar = NavigationToolbar(self.canvas, self)
        # self.ax = self.fig.add_subplot(111)
        # self.ax.grid()
        # self.ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        # self.ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        # self.ax.set_xlabel('t(s)')
        # self.ax.set_ylabel('N')
        # self.ax.set_title("Live Graph")
        self.customFig = CustomFigCanvas()

        # setup the grid layout design and components
        self.vbox_graph = QVBoxLayout()
        # self.vbox_graph.addWidget(self.customFig.toolbar)
        self.vbox_graph.addWidget(self.customFig)

    def plotGraph(self, data):
        # plot the graph and set the labels
        status = processData(data)
        self.time += 1

        features = []
        self.angry.append(status["angry"])
        self.disgust.append(status["disgust"])
        self.fear.append(status["fear"])
        self.happy.append(status["happy"])
        self.sad.append(status["sad"])
        self.surprise.append(status["surprise"])
        self.neutral.append(status["neutral"])
        self.focus.append(status["focus"])

        features.append(self.angry)
        features.append(self.disgust)
        features.append(self.fear)
        features.append(self.happy)
        features.append(self.sad)
        features.append(self.surprise)
        features.append(self.neutral)
        features.append(self.focus)

        t = np.linspace(1, self.time, num=self.time)

        for i in range(len(self.features)):
            y = np.array(features[i])
            self.ax.plot(t, y, label=self.features[i][0], color=self.features[i][1])
            self.ax.legend(bbox_to_anchor=(0.9, 1.1), loc='upper left', borderaxespad=0.)


class CustomFigCanvas(FigureCanvas, TimedAnimation):
    def __init__(self):
        self.features = [('angry', '#1f77b4'),
                         ('disgust', '#ff7f0e'),
                         ('fear', '#2ca02c'),
                         ('happy', '#d62728'),
                         ('sad', '#9467bd'),
                         ('surprise', '#8c564b'),
                         ('neutral', '#e377c2'),
                         ('focus', '#7f7f7f')]
        self.angry = []
        self.disgust = []
        self.fear = []
        self.happy = []
        self.sad = []
        self.surprise = []
        self.neutral = []
        self.focus = []
        self.time = 0

        self.fig = Figure(figsize=(9, 7), dpi=65, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        self.ax = self.fig.add_subplot(111)
        self.ax.grid()
        self.ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        self.ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        self.ax.set_xlabel('t(s)')
        self.ax.set_ylabel('N')
        self.ax.set_title("Live Graph")

        self.line1 = Line2D([], [], color=self.features[0][1], linewidth=2)
        self.line2 = Line2D([], [], color=self.features[1][1], linewidth=2)
        self.line3 = Line2D([], [], color=self.features[2][1], linewidth=2)
        self.line4 = Line2D([], [], color=self.features[3][1], linewidth=2)
        self.line5 = Line2D([], [], color=self.features[4][1], linewidth=2)
        self.line6 = Line2D([], [], color=self.features[5][1], linewidth=2)
        self.line7 = Line2D([], [], color=self.features[6][1], linewidth=2)
        self.line8 = Line2D([], [], color=self.features[7][1], linewidth=2)

        self.ax.add_line(self.line1)
        self.ax.add_line(self.line2)
        self.ax.add_line(self.line3)
        self.ax.add_line(self.line4)
        self.ax.add_line(self.line5)
        self.ax.add_line(self.line6)
        self.ax.add_line(self.line7)
        self.ax.add_line(self.line8)

        FigureCanvas.__init__(self, self.fig)
        TimedAnimation.__init__(self, self.fig, interval=50, blit=True)

    def new_frame_seq(self):
        return iter(range(self.time))

    def _init_draw(self):
        lines = [self.line1, self.line2, self.line3, self.line4,
                 self.line5, self.line6, self.line7, self.line8]

        for line in lines:
            line.set_data([], [])

    def addData(self, data):
        status = processData(data)
        self.time += 1

        self.angry.append(status["angry"])
        self.disgust.append(status["disgust"])
        self.fear.append(status["fear"])
        self.happy.append(status["happy"])
        self.sad.append(status["sad"])
        self.surprise.append(status["surprise"])
        self.neutral.append(status["neutral"])
        self.focus.append(status["focus"])

    def _step(self, *args):
        # extends the _step() method for the TimedAnimation class
        try:
            TimedAnimation._step(self, *args)
        except:
            TimedAnimation._stop(self)

    def _draw_frame(self, framedata):
        t = np.linspace(1, self.time, num=self.time)
        self.line1.set_data(t, self.angry)
        self.line2.set_data(t, self.disgust)
        self.line3.set_data(t, self.fear)
        self.line4.set_data(t, self.happy)
        self.line5.set_data(t, self.sad)
        self.line6.set_data(t, self.surprise)
        self.line7.set_data(t, self.neutral)
        self.line8.set_data(t, self.focus)
        self._drawn_artists = [self.line1, self.line2, self.line3, self.line4,
                               self.line5, self.line6, self.line7, self.line8]

class Communicate(QObject):
    data_signal = pyqtSignal(list)


def generateRandData():
    n = 1000
    data = []
    for i in range(n):
        status = {"angry": round(np.random.rand()),
                  "disgust": round(np.random.rand()),
                  "fear": round(np.random.rand()),
                  "happy": round(np.random.rand()),
                  "sad": round(np.random.rand()),
                  "surprise": round(np.random.rand()),
                  "neutral": round(np.random.rand()),
                  "focus": round(np.random.rand())}
        data.append(status)

    return data

def dataSend(addData_callbackFunc):
    # setup the signal-slot mechanism.
    signal = Communicate()
    signal.data_signal.connect(addData_callbackFunc)

    for i in range(1000):
        data = generateRandData()
        time.sleep(0.1)
        signal.data_signal.emit(data)


# run the application and show the window
app = QApplication(sys.argv)
window = Live_Graph()
window.show()


app.exec_()
sys.exit(0)