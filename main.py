from flask import Flask, jsonify, request
from services import firebase

app = Flask(__name__)


@app.route("/hello")
def home():
    return "Hello Awkward World!"


@app.route("/vehicle")
def get_vehicle():
    vid = request.args.get("vid")
    if vid != "":
        response = firebase.get_vehicle(vid)
    else:
        response = "Please provide VID"
    return jsonify(response)


if __name__ == "__main__":
    app.run()
