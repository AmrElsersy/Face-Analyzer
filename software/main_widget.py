from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5 import QtGui
from software.live_graph import Live_Graph
from software.live_hist import Live_Histogram
from software.pie_chart import GazeTrackingChart
import sys

from software.utils import data_send, Thread
import threading


class Live_Statistics(QWidget):
    def __init__(self, url):
        # call the constructor of the parent (QWidget)
        super(Live_Statistics, self).__init__()

        self.interval = 1000

        # set title  and geometry for the window
        self.setWindowTitle("Live Statistics")
        self.setGeometry(500, 400, 800, 600)

        # give orange background to the window
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(0, 128, 128))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # set minimum width and height for the window
        self.setMinimumHeight(600)
        self.setMinimumWidth(800)
        self.setMaximumHeight(600)
        self.setMaximumWidth(800)

        # set icon for the application at run time and center the application window with the primary screen
        self.setIcon()
        self.center()

        self.createTabs()

        signal = Thread()
        signal.thread_signal.connect(self.addData_callbackFunc)

        dataSend = threading.Thread(name='data_send', target=data_send, daemon=True,
                                    args=(url, signal))
        dataSend.start()

    def addData_callbackFunc(self, data):
        self.live_graph.customFig.addData(data)
        self.live_hist.customFig.addData(data)
        self.gaze_chart.addData(data)

    def createTabs(self):
        self.layout = QVBoxLayout()
        self.live_graph = Live_Graph(self.interval)
        self.live_hist = Live_Histogram(self.interval)
        self.gaze_chart = GazeTrackingChart()
        self.tabs = QTabWidget()
        self.tabs.addTab(self.live_graph, QIcon("graph.png"), "Live Graph")
        self.tabs.addTab(self.live_hist, QIcon("hist.png"), "Live Histogram")
        self.tabs.addTab(self.gaze_chart, QIcon("pie.png"), "Live Gaze-Tracking")
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    # set icon for the application
    def setIcon(self):
        appIcon = QIcon("stat.png")
        self.setWindowIcon(appIcon)

    # to center the application window at the beginning
    def center(self):
        qRect = self.frameGeometry()
        centerPoint = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qRect.moveCenter(centerPoint)
        self.move(qRect.topLeft())

#
# def main():
#     app = QApplication(sys.argv)
#     main = Live_Statistics()
#     main.show()
#     sys.exit(app.exec_())
#
# if __name__ == "__main__":
#     main()