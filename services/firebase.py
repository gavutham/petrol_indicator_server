import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("D:/coding/Python Projects/petrol_server/petrol_indicator_server/utils/cred.json")
firebase_admin.initialize_app(cred)

db = firestore.client() 

def get_vehicle(vid):
    vehicle_collection_ref = db.collection("vehicles").document(vid)

    try:
        res = vehicle_collection_ref.get()
        return res.data
    except Exception:
        return "Some Error occurred"
def fuel_level(vid,h):
    data={"fuellevel":h}
    fuel_level_reference = db.collection("fuellevel").document(vid)
    try:
        fuel_level_reference.set(data)
    except Exception as error:
        return error
    
def fuel_volume(vid):
    fuel_level_reference = db.collection("fuellevel").document(vid)
    vehicle_collection_ref = db.collection("vehicles").document(vid)

    try:
        res = fuel_level_reference.get()
        fuel_level = res._data
        res = vehicle_collection_ref.get()
        vehicle =res._data
        
    except Exception as error:
        return error
    
    return {"vehicle": dict(vehicle), "fuel_level": fuel_level["fuellevel"]}




