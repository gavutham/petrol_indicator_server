import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("D:/works/python projects/petrol_indicator_server/utils/cred.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def get_vehicle(vid):
    vehicle_collection_ref = db.collection("vehicles").document(vid)

    try:
        res = vehicle_collection_ref.get()
        return res.data
    except Exception:
        return "Some Error occurred"
