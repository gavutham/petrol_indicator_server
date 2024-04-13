import firebase_admin
from firebase_admin import credentials, firestore, storage
from datetime import datetime
import io
import joblib
import pprint


cred = credentials.Certificate("D:/works/python projects/petrol_indicator_server/utils/cred.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
storage_client = storage.bucket("petrol-indicator.appspot.com")


def set_fuel_level(vid,h):
    vehicle_ref = db.collection("vehicles").document(vid)
    fuel_level_reference = db.collection("fuellevel").document(vid)
    try:
        res = vehicle_ref.get()
        height = int(res.data["height"])

        print(height, h)

        data = {"fuellevel": height-h}
        fuel_level_reference.set(data)
    except Exception as error:
        return error


def fuel_volume(vid):
    fuel_level_reference = db.collection("fuellevel").document(vid)
    vehicle_collection_ref = db.collection("vehicles").document(vid)
    

    try:
        res = fuel_level_reference.get()
        fuel_level = res.data
        res = vehicle_collection_ref.get()
        vehicle = res.data
        
    except Exception as error:
        return error
    
    return {"vehicle": dict(vehicle), "fuel_level": fuel_level["fuellevel"]}


def set_refill(vid, data):
    refill_ref = db.collection("refill").document(vid).collection(data["time"]).document(data["time"])

    try:
        refill_ref.set(data)
        return "Refill updated successfully"
    except Exception as error:
        print(error)
        return "Some error occurred while setting refill"


def get_refill(vid, date):
    refill_ref = db.collection("refill").document(vid).collection(date).document(date)

    try:
        res = refill_ref.get()
        return res.data
    except Exception as error:
        print(error)
        return "error at retrieving refill doc"


def get_efficient_gps(vid):
    refill_ref = db.collection("refill").document(vid)
    collections = refill_ref.collections()
    timestamps = []

    for collection in collections:
        time = str(collection.id).replace("'", "").replace('"', "")
        date_object = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        timestamps.append(date_object)
    timestamps.sort(reverse=True)

    past_refills = [x.strftime('%Y-%m-%d %H:%M:%S') for x in timestamps[:10]]

    refill_data = [get_refill(vid, doc) for doc in past_refills]

    max_index = -1
    max_mileage = -1

    for i in range(1, 10):
        km = int(refill_data[i-1]["kilometers"]) - int(refill_data[i]["kilometers"])
        fuel = int(refill_data[i]['after']) - int(refill_data[i-1]["before"])
        mileage = km/fuel

        if mileage > max_mileage:
            max_index = i
            max_mileage = mileage

    return refill_data[max_index]["latitude"], refill_data[max_index]["longitude"]


def save_model(model, vid):
    try:
        stream = io.BytesIO()

        joblib.dump(model, stream)
        stream.seek(0)

        blob = storage_client.blob(f"models/{vid}.pkl")
        blob.upload_from_file(stream, content_type='application/octet-stream')

        print("model saved")
    except Exception as ex:
        print(ex)


def retrieve_model(vid):
    try:
        path = f"models/{vid}.pkl"
        stream = io.BytesIO()

        blob = storage_client.blob(path)
        blob.download_to_file(stream)

        stream.seek(0)

        model = joblib.load(stream)

        return model

    except Exception as ex:
        print(ex)


def get_all_refills(vid):
    refill_ref = db.collection("refill").document(vid)
    collections = refill_ref.collections()
    timestamps = []

    for collection in collections:
        time = str(collection.id).replace("'", "").replace('"', "")
        date_object = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        timestamps.append(date_object)
    timestamps.sort(reverse=True)

    past_refills = [x.strftime('%Y-%m-%d %H:%M:%S') for x in timestamps]

    refill_data = [get_refill(vid, doc) for doc in past_refills]

    return  refill_data


def predict_kilometers(vid):
    fuel_level_reference = db.collection("fuellevel").document(vid)

    try:
        res = fuel_level_reference.get()
        level = int(res.data["fuellevel"])

        model = retrieve_model(vid)
        predictions = float(model.predict([[level]])[0])

        return {"km": float(format(predictions, ".2f"))}
    except Exception as error:
        print(error)
        return "error occurred"
