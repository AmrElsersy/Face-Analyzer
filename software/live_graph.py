# import required library for GUI
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QCheckBox
from PyQt5.QtGui import QFont, QPalette, QColor

# import matplotlib backend and figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.animation import TimedAnimation
from matplotlib.ticker import MaxNLocator

from software.utils import processData, Status

import matplotlib
import numpy as np

matplotlib.use("Qt5Agg")

class Live_Graph(QWidget):
    def __init__(self, interval):
        # call the constructor of the parent (QWidget)
        super(Live_Graph, self).__init__()

        self.read_status = Status()

        # # give orange background to the window
        # palette = self.palette()
        # palette.setColor(QPalette.Window,QColor(0, 128, 128))
        # self.setPalette(palette)
        # self.setAutoFillBackground(True)

        # setup the grid layout design and components
        self.createPlotLayout(interval)
        self.createCheckboxes()
        self.hbox = QHBoxLayout()
        self.hbox.addLayout(self.vbox_graph)
        self.hbox.addWidget(self.groupBox)
        self.setLayout(self.hbox)

        self.angry_cb.stateChanged.connect(self.get_status)
        self.disgust_cb.stateChanged.connect(self.get_status)
        self.fear_cb.stateChanged.connect(self.get_status)
        self.happy_cb.stateChanged.connect(self.get_status)
        self.sad_cb.stateChanged.connect(self.get_status)
        self.surprise_cb.stateChanged.connect(self.get_status)
        self.neutral_cb.stateChanged.connect(self.get_status)
        self.focus_cb.stateChanged.connect(self.get_status)
        self.read_status.status_signal.connect(self.customFig.read_status)

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

    def createPlotLayout(self, interval):
        self.customFig = CustomFigGraph(interval)
        self.toolbar = NavigationToolbar(self.customFig, self)

        # setup the grid layout design and components
        self.vbox_graph = QVBoxLayout()
        self.vbox_graph.addWidget(self.toolbar)
        self.vbox_graph.addWidget(self.customFig)

    def get_status(self):
        status = [self.angry_cb.isChecked(), self.disgust_cb.isChecked(), self.fear_cb.isChecked(),
                  self.happy_cb.isChecked(), self.sad_cb.isChecked(), self.surprise_cb.isChecked(),
                  self.neutral_cb.isChecked(), self.focus_cb.isChecked()]

        self.read_status.status_signal.emit(status)

class CustomFigGraph(FigureCanvas, TimedAnimation):
    def __init__(self, interval):
        self.features = [('angry', '#1f77b4'),
                         ('disgust', '#ff7f0e'),
                         ('fear', '#2ca02c'),
                         ('happy', '#d62728'),
                         ('sad', '#9467bd'),
                         ('surprise', '#8c564b'),
                         ('neutral', '#e377c2'),
                         ('focus', '#7f7f7f')]
        self.status = [True] * 8
        self.lines = []

        self.current_features = [np.array([])] * 8
        self.time = 0
        self.interval = interval

        self.fig = Figure(figsize=(11, 9), dpi=100, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel('t(s)')
        self.ax.set_ylabel('N')
        self.ax.set_title("Live Graph")
        self.ax.grid(linestyle='--', linewidth=0.5)
        self.ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        self.ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)

        for i in range(len(self.current_features)):
            self.lines.append(Line2D([], [], color=self.features[i][1]))

        for line in self.lines:
            self.ax.add_line(line)

        features = [feature[0] for feature in self.features]
        self.ax.legend(self.lines, features, bbox_to_anchor=(0.915, 1.15), loc='upper left', borderaxespad=0.)

        FigureCanvas.__init__(self, self.fig)
        TimedAnimation.__init__(self, self.fig, interval=self.interval, blit=False)

    def read_status(self, status):
        self.status = status

    def new_frame_seq(self):
        it = iter(range(int(self.time/int(self.interval/1000))))
        return it

    def _init_draw(self):
        for line in self.lines:
            line.set_data([], [])

    def addData(self, data):
        status = processData(data)
        print("Live Graph: ", status)
        self.time += int(self.interval/1000)

        for i in range(len(self.current_features)):
            self.current_features[i] = np.append(self.current_features[i], status[self.features[i][0]])

    def _step(self, *args):
        # extends the _step() method for the TimedAnimation class
        try:
            TimedAnimation._step(self, *args)
        except:
            TimedAnimation._stop(self)

    def _draw_frame(self, framedata):
        arrays = [arr for i, arr in enumerate(self.current_features) if self.status[i]]
        ylim_max = np.maximum.reduce(arrays).max() + 5
        ylim_min = np.minimum.reduce(arrays).min() - 5
        self.ax.set_xlim(1, self.time)
        self.ax.set_ylim(max(ylim_min, 0), ylim_max)

        t = np.linspace(1, self.time, num=int(self.time/int(self.interval/1000)))

        lines = []
        for i in range(len(self.current_features)):
            self.lines[i].set_data(t, self.current_features[i])
            if not self.status[i]:
                self.lines[i].set_visible(False)
            else:
                self.lines[i].set_visible(True)
                lines.append(self.lines[i])

        features = [feature[0] for i, feature in enumerate(self.features) if self.status[i]]
        self.ax.legend(lines, features, bbox_to_anchor=(0.915, 1.15), loc='upper left', borderaxespad=0.)

        self._drawn_artists = self.lines