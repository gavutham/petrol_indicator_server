import firebase_admin
from firebase_admin import credentials, firestore, storage
import joblib
import io

cred = credentials.Certificate("D:/works/python projects/petrol_indicator_server/utils/cred.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
storage_client = storage.bucket("petrol-indicator.appspot.com")


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
        print("model retrieved")

        return model

    except Exception as ex:
        print(ex)


def get_vehicle(vid):
    vehicle_collection_ref = db.collection("vehicles").document(vid)

    try:
        res = vehicle_collection_ref.get()
        return res.data
    except Exception:
        return "Some Error occurred"
