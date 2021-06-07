

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