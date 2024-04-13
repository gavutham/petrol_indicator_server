import datetime
from flask import Flask, jsonify, request
from services import firebase
import math

app = Flask(__name__)


@app.route("/fuellevel")
def fuel_level():
    vid = request.args.get("vid")
    level = request.args.get("h")

    if vid is not None and level is not None:
        firebase.set_fuel_level(vid, level)
        return "Fuel level set successfully"
    else:
        if vid is None:
            response = "Please provide VID "
        else:
            response = "Please provide level"
        return response


@app.route("/fuelvolume")
def fuel_volume():
    vid = request.args.get("vid")
    if vid is not None:
        response = firebase.fuel_volume(vid)
        vehicle = response['vehicle']

        tank_type = ["fueltank_shape"]

        if tank_type == "Cuboid":
            b = float(vehicle["breadth"])
            l = float(vehicle["length"])
            h = float(response["fuel_level"])

            return {"volume": float(format(l*b*h/1000, ".2f"))}
        else:
            d = float(vehicle["diameter"])
            h = float(response["fuel_level"])

            return {"volume": float(format((math.pi * d**2 * h) / 4000, ".2f"))}


@app.route("/refill")
def refill():
    vid = request.args.get("vid")
    lat = request.args.get("lat")
    long = request.args.get("long")
    kilometer = request.args.get("kilometer")
    before = request.args.get("before")
    after = request.args.get("after")

    data = {
        "latitude": lat,
        "longitude": long,
        "kilometer": kilometer,
        "before": before,
        "after": after,
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return firebase.set_refill(vid, data)


@app.route("/efficient")
def efficient_location():
    vid = request.args.get("vid")
    (lat, long) = firebase.get_efficient_gps(vid)
    return {"lat": lat, "long": long}


@app.route("/predict")
def predict():
    vid = request.args.get("vid")
    return firebase.predict_kilometers(vid)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
