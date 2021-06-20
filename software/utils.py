from PyQt5.QtCore import QObject, pyqtSignal
import numpy as np
import time

class Worker(QObject):
    thread_signal = pyqtSignal(list)

class Status(QObject):
    status_signal = pyqtSignal(list)

def normalize_state(state):
    out = 0
    if state == 0:
        out = 20
    else:
        out = state*20 + 20

    return out

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
        status["angry"] += normalize_state(el["angry"])
        status["disgust"] += normalize_state(el["disgust"])
        status["fear"] += normalize_state(el["fear"])
        status["happy"] += normalize_state(el["happy"])
        status["sad"] += normalize_state(el["sad"])
        status["surprise"] += normalize_state(el["surprise"])
        status["neutral"] += normalize_state(el["neutral"])
        status["focus"] += normalize_state(el["focus"])

    return status

def processGazeTracking(data):
    status = {"not focus": 0,
              "focus": 0}

    for el in data:
        status["not focus"] += normalize_state(el["not focus"])
        status["focus"] += normalize_state(el["focus"])

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

