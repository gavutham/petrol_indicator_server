from flask import Flask, jsonify, request
from services import firebase
import math

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

@app.route("/fuellevel")
def fuel_level():
    vid = request.args.get("vid")
    level = request.args.get("h")
    print(vid,level)
    if vid != None and level!=None:
        response = firebase.fuel_level(vid,level)
        return "Fuel level set successfully"
    else:
        if vid == None:
            response = "Please provide VID "
        if level == None:
            response = "Please provide level"
        return response
@app.route("/fuelvolume")
def fuel_volume():
    vid = request.args.get("vid")
    if vid!= None:
        response = firebase.fuel_volume(vid)
        vehicle =  response['vehicle']

        tank_type =["fueltank_shape"]

        if tank_type == "Cuboid":
            b =  int(vehicle["breadth"])
            l =  int(vehicle["length"])
            h = int(vehicle["height"]) - int(response["fuel_level"])

            return {"volume": l*b*h/1000}
        else:
            d = int(vehicle["diameter"])
            h = int(vehicle["height"]) - int(response["fuel_level"])

            return {"volume": (math.pi * d**2 * h) / 4000}

    
if __name__ == "__main__":
    app.run(debug=True)
