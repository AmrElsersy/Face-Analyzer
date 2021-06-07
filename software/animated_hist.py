import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal

# import matplotlib backend and figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.animation import TimedAnimation, FuncAnimation
from matplotlib.ticker import MaxNLocator

import time
import threading
import random




def generateRandData(low=0, high=100):
    data = [(random.randint(low, high)),
            (random.randint(low, high)),
            (random.randint(low, high)),
            (random.randint(low, high)),
            (random.randint(low, high)),
            (random.randint(low, high)),
            (random.randint(low, high))
            ]

    return data



class Thread(QObject):
    thread_signal = pyqtSignal(list)

class Status(QObject):
    status_signal = pyqtSignal(list)

# Ensure using PyQt5 backend
import matplotlib
matplotlib.use('QT5Agg')

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon
from utils import processData

class Histogram(FigureCanvas):
    def __init__(self):
        self.features = ['angry','disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        # self.fig, self.ax = self.__create_hist()
        self.fig, ax = plt.subplots()
        self.patches = ax.bar(self.features, generateRandData() ,lw=1, ec="yellow", fc="green", alpha=0.5)
    
    def add_data(self, data):
        ani = animation.FuncAnimation(self.fig, self.__animate(self.patches, data), blit=True, interval=100,
                                            frames=10,
                                            repeat=False)
        plt.show()

    def __create_hist(self):
        fig, ax = plt.subplots()
        self.patches = ax.bar(self.features, generateRandData() ,lw=1, ec="yellow", fc="green", alpha=0.5)
        return fig, ax

    def __animate(self, patches, data):
        for rect, h in zip(patches, data):
            rect.set_height(h)
        return patches


# hist = Histogram()
# frames = 10
# for i in range(frames):
#     print(i)
#     hist.add_data(generateRandData())

# plt.show()
# import sys
# def main():
#     app = QtWidgets.QApplication(sys.argv)
#     main = Histogram()
#     # main = MainWidget()
#     main.show()
#     sys.exit(app.exec_())
    
    
# if __name__ == "__main__":
#     main()


def dataSend(addData_callbackFunc):
    # setup the signal-slot mechanism.
    signal = Thread()
    signal.thread_signal.connect(addData_callbackFunc)
    n = 1000
    for i in range(n):
        data = generateRandData(n)
        time.sleep(1)
        signal.thread_signal.emit(data)


def animate(frameno):
    n = generateRandData()
    for rect, h in zip(patches, n):
        rect.set_height(h)
    return patches

fig, ax = plt.subplots()


features = ['angry','disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

# print(bar_container)
patches = ax.bar(features, generateRandData() ,lw=1, ec="yellow", fc="green", alpha=0.5)
frames = 100
ani = animation.FuncAnimation(fig, animate, blit=True, interval=100,
                              frames=10,
                              repeat=False)
plt.show()
