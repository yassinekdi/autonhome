import os
import requests
import schedule 
# import pyrebase
from dotenv import load_dotenv
import time
from pytz import timezone
from datetime import datetime
import sys
from pathlib import Path
import firebase_admin
from firebase_admin import credentials, db, storage
# from PIL import Image
from io import BytesIO

autonhome_dir = Path(__file__).resolve().parents[1]
serre_path = os.path.join(autonhome_dir)
sys.path.append(serre_path)

from serre.constants import measures_metadata

# Charge les variables d'environnement
load_dotenv()


class RealtimeFirebaseSync:

    def __init__(self, timezone_area='Europe/Paris'):
        """
        Initialize FirebaseSync with environment variables
        """
        self.FIREBASE_HOST = os.getenv("FIREBASE_HOST")
        self.DJANGO_API = os.getenv("DJANGO_API")
        self.DJANGO_USERNAME = os.getenv("DJANGO_USERNAME")
        self.DJANGO_USER_ID = os.getenv("DJANGO_USER_ID")
        self.DJANGO_PASSWORD = os.getenv("DJANGO_PASSWORD")
        self.SERVICE_ACCOUNT_KEY = os.getenv("SERVICE_ACCOUNT_KEY", )
        self.timezone = timezone(timezone_area)
        firebase_scount_path = os.path.join(serre_path,'syncs','service-account.json')
        # Initialize Firebase
        cred = credentials.Certificate(firebase_scount_path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': self.FIREBASE_HOST
        })
        self.auth_token = self.get_auth_token()
        self.api_header = self.get_auth_header()
        self.sensors = []

    def get_auth_token(self):
        """
        Authenticate with Django API and get JWT token
        """
        response = requests.post(f"{self.DJANGO_API}/token/", 
                                 data={"username": self.DJANGO_USERNAME, "password": self.DJANGO_PASSWORD})
        return response.json()["access"]

    def fetch_data_from_firebase(self, node):
        """
        Fetch data from Firebase from specified node
        """
        ref = db.reference(node)
        return ref.get()

    def convert_timestamp(self, timestamp_int):
        """
        Converts a Firebase timestamp to a Python datetime object.
        """
        utc_time = datetime.utcfromtimestamp(timestamp_int)
        local_time = utc_time.replace(tzinfo=timezone('UTC')).astimezone(self.timezone)
        return local_time

    def create_Measure(self, data, headers):
        """
        Send a POST request to the Django API to create a new Measure instance.
        """
        response = requests.post(f"{self.DJANGO_API}/measures/", json=data, headers=headers)
        print(response.status_code, response.json())

    def get_sensors(self):
        """
        Retrieve all sensor instances from Django API
        """
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = requests.get(f"{self.DJANGO_API}/sensors/", headers=headers)
        self.sensors = response.json()

    def get_sensor_id(self, sensor_name):
        """
        Retrieve the ID of a sensor with the given name
        """
        for sensor in self.sensors:
            if sensor["name"] == sensor_name:
                return sensor["id"]
        return None

    def sync(self):
        """
        Fetch data from Firebase, process it and create new Measure instances
        in the
        """
        try:
            self.get_sensors()
            for sensor in self.sensors:
                node=f"{self.DJANGO_USER_ID}/{sensor['section']}/{sensor['name']}"
                firebase_data = self.fetch_data_from_firebase(node)

                for measure_key in firebase_data:                
                    measure = firebase_data[measure_key]
                    data = self.process_firebase_data(measure, sensor['id'])              
                    for measure_data in data:              
                        self.create_Measure(measure_data, headers=self.api_header) # Send post request to API to create Measure instance.

        except Exception as e:
            print(' ')
            print(f"Une erreur s'est produite lors de la synchronisation des données: {e}")

    def get_auth_header(self):
        return {"Authorization": f"Bearer {self.auth_token}"}

    def process_firebase_data(self, firebase_measure, sensor_id):
        """
        Process a single measure from Firebase, converting it into the data format
        required by the Django API.
        """
        timestamp_int = firebase_measure['timestamp']  
        timestamp = self.convert_timestamp(timestamp_int)

        data = []
        for measure_name, metadata in measures_metadata.items():
            if measure_name in firebase_measure:
                measure_data = {
                    "sensor": sensor_id,
                    "value": firebase_measure[measure_name],
                    "timestamp": timestamp.isoformat(),
                    "label": metadata["label"],
                    "unit": metadata["unit"],
                    "user": self.DJANGO_USER_ID,
                }
                data.append(measure_data)

        return data



class FirebaseStorageSync:

    def __init__(self):
        """
        Initialize ImageCapture with provided arguments
        """
        IP_address = os.getenv("IP_ADRESS")
        self.url = IP_address + "capture"
        self.DJANGO_USER_ID = os.getenv("DJANGO_USER_ID")
        self.SERVICE_ACCOUNT_KEY = os.getenv("SERVICE_ACCOUNT_KEY", )
        firebase_scount_path = os.path.join(serre_path,'syncs','service-account.json')

        # Initialize Firebase
        cred = credentials.Certificate(firebase_scount_path)
        firebase_admin.initialize_app(cred, {
            'storageBucket': os.getenv("FIREBASE_STORAGE_BUCKET")
        })

        # Get the storage bucket
        self.bucket = storage.bucket()

    def sync(self):
        """
        Capture image from provided url and save it to Firebase Storage
        """
        try:
            response = requests.get(self.url)
            image_data = BytesIO(response.content)

            # Get current time and format it
            now = datetime.now()
            formatted_time = now.strftime("%H_%d_%m_%Y")

            image_name = f'capt_{formatted_time}.jpg'
            print(f"Image capturée à {time.ctime()}")

            # Create a new blob and upload the image's content.
            blob = self.bucket.blob(f"{self.DJANGO_USER_ID}/{image_name}")
            blob.upload_from_file(image_data, content_type='image/jpg')

        except Exception as e:
            print(f"Une erreur est survenue: {e}")



if __name__ == "__main__":
    # REALTIME FIREBASE 
    realtime_syncer = RealtimeFirebaseSync()
    # STORAGE FIREBASE
    storage_syncer = FirebaseStorageSync()

    # Planifie l'exécution de la fonction toutes les 10 secondes
    schedule.every(10).seconds.do(realtime_syncer.sync)
    schedule.every(10).seconds.do(storage_syncer.sync)

    # Boucle infinie pour exécuter les tâches planifiées
    while True:
        schedule.run_pending()
        time.sleep(1)
