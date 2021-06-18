from PyQt5.QtCore import QObject, pyqtSignal
import numpy as np
import time

class Worker(QObject):
    thread_signal = pyqtSignal(list)

class Status(QObject):
    status_signal = pyqtSignal(list)

def processData(data):
    status = {"angry": 0,
              "disgust": 0,
              "fear": 0,
              "happy": 0,
              "sad": 0,
              "surprise": 0,
              "neutral": 0,
              "focus": 0}

    for el in data:
        status["angry"] += el["angry"]
        status["disgust"] += el["disgust"]
        status["fear"] += el["fear"]
        status["happy"] += el["happy"]
        status["sad"] += el["sad"]
        status["surprise"] += el["surprise"]
        status["neutral"] += el["neutral"]
        status["focus"] += el["focus"]

    return status

def processGazeTracking(data):
    status = {"not focus": 0,
              "focus": 0}

    for el in data:
        status["not focus"] += el["not focus"]
        status["focus"] += el["focus"]

    return status

def dataSend(addData_callbackFunc, interval):
    # setup the signal-slot mechanism.
    signal = Worker()
    signal.thread_signal.connect(addData_callbackFunc)
    n = 1000
    for i in range(n):
        data = generateRandData(n)
        time.sleep(interval/1000)
        signal.thread_signal.emit(data)

def generateRandData(n):
    data = []
    for i in range(n):
        status = {"angry": round(np.random.rand()),
                  "disgust": round(np.random.rand()),
                  "fear": round(np.random.rand()),
                  "happy": round(np.random.rand()),
                  "sad": round(np.random.rand()),
                  "surprise": round(np.random.rand()),
                  "neutral": round(np.random.rand()),
                  "focus": round(np.random.rand()),
                  "not focus": round(np.random.rand())}
        data.append(status)

    return data

