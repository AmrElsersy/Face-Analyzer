from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)


@app.route("/",methods=["GET", "POST"])
def add_face_info():
    # json = request.get_json()

    return jsonify ({
        "id":3
        })

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8008)