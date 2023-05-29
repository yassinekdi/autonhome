import os
import requests
import schedule 
import pyrebase
from dotenv import load_dotenv
import time
from pytz import timezone
from datetime import datetime
import sys
from pathlib import Path

import requests
from PIL import Image
from io import BytesIO

autonhome_dir = Path(__file__).resolve().parents[1]
serre_path = os.path.join(autonhome_dir)
sys.path.append(serre_path)

from serre.constants import europe_paris_timezone, measures_metadata

# Charge les variables d'environnement
load_dotenv()

class RealtimeFirebaseSync:

    def __init__(self,timezone_area=europe_paris_timezone):
        """
        Initialize FirebaseSync with environment variables
        """
        self.FIREBASE_HOST = os.getenv("FIREBASE_HOST")
        self.FIREBASE_AUTH = os.getenv("FIREBASE_AUTH")
        self.DJANGO_API = os.getenv("DJANGO_API")
        self.DJANGO_USERNAME = os.getenv("DJANGO_USERNAME")
        self.DJANGO_USER_ID = os.getenv("DJANGO_USER_ID")
        self.DJANGO_PASSWORD = os.getenv("DJANGO_PASSWORD")
        self.FIREBASE_AUTH_DOMAIN = os.getenv("FIREBASE_AUTH_DOMAIN")
        self.FIREBASE_STORAGE_BUCKET = os.getenv("FIREBASE_STORAGE_BUCKET")
        self.timezone=timezone(timezone_area)

        self.config = {
            "apiKey": self.FIREBASE_AUTH,
            "authDomain": self.FIREBASE_AUTH_DOMAIN,
            "databaseURL": self.FIREBASE_HOST,
            "storageBucket": self.FIREBASE_STORAGE_BUCKET,
        }


        self.firebase = pyrebase.initialize_app(self.config)
        self.db = self.firebase.database()

    def get_auth_token(self):
        """
        Authenticate with Django API and get JWT token
        """
        response = requests.post("http://localhost:8000/api/token/", data={"username": self.DJANGO_USERNAME, "password": self.DJANGO_PASSWORD})
        return response.json()["access"]

    def fetch_data_from_firebase(self,node):
        """
        Fetch data from Firebase from specified node with authentication
        """
        auth_token = self.get_auth_token()
        measures = self.db.child(node).get()
        headers = {"Authorization": f"Bearer {auth_token}"}
        return {'measures': measures, 'headers': headers}

    def convert_timestamp(self, timestamp_int):
        """
        Converts a Firebase timestamp to a Python datetime object.
        """
        utc_time = datetime.utcfromtimestamp(timestamp_int)
        local_time = utc_time.replace(tzinfo=timezone('UTC')).astimezone(self.timezone)
        return local_time
    
    def create_Measure(self,data,headers):
        """
        Send a POST request to the Django API to create a new Measure instance.
        """
        response = requests.post(self.DJANGO_API, json=data, headers=headers)
        print(response.status_code, response.json())

    def get_sensors(self):
        """
        Retrieve all sensor instances from Django API
        """
        headers = {"Authorization": f"Bearer {self.get_auth_token()}"}
        response = requests.get(self.DJANGO_API+"/sensors/", headers=headers)
        return response.json()

    def get_sensor_id(self, sensor_name):
        """
        Retrieve the ID of a sensor with the given name
        """
        sensors = self.get_sensors()
        for sensor in sensors:
            if sensor["name"] == sensor_name:
                return sensor["id"]
        return None

    def sync(self):
        """
        Fetch data from Firebase, process it and create new Measure instances
        in the
        """
        try:
            sensors = self.get_sensors()
            for sensor in sensors:
                node=f"{self.DJANGO_USER_ID}/{sensor['section']}/{sensor['name']}"
                firebase_data = self.fetch_data_from_firebase(node)

                for measure in firebase_data['measures'].each():                
                    data = self.process_firebase_data(measure, sensor['id'])                
                    for measure_data in data:              
                        self.create_Measure(measure_data, firebase_data['headers']) # Send post request to API to create Measure instance.
                                
        except Exception as e:
            print(' ')
            print(f"Une erreur s'est produite lors de la synchronisation des données: {e}")

    def process_firebase_data(self,firebase_measure, sensor_id):
        """
        Process a single measure from Firebase, converting it into the data format
        required by the Django API.
        """
        timestamp_int = firebase_measure.val()['timestamp']  
        timestamp = self.convert_timestamp(timestamp_int) 

        data = []
        for measure_name, metadata in measures_metadata.items():
            if measure_name in firebase_measure.val():
                measure_data = {
                    "sensor": sensor_id,
                    "value": firebase_measure.val()[measure_name],
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
        IP_adress = os.getenv("IP_ADRESS")
        self.url = IP_adress + "capture"
        
        self.FIREBASE_HOST = os.getenv("FIREBASE_HOST")
        self.FIREBASE_AUTH = os.getenv("FIREBASE_AUTH")
        self.DJANGO_USER_ID = os.getenv("DJANGO_USER_ID")
        self.FIREBASE_AUTH_DOMAIN = os.getenv("FIREBASE_AUTH_DOMAIN")
        self.FIREBASE_STORAGE_BUCKET = os.getenv("FIREBASE_STORAGE_BUCKET")

        self.config = {
            "apiKey": self.FIREBASE_AUTH,
            "authDomain": self.FIREBASE_AUTH_DOMAIN,
            "databaseURL": self.FIREBASE_HOST,
            "storageBucket": self.FIREBASE_STORAGE_BUCKET,
        }

        self.firebase = pyrebase.initialize_app(self.config)
        self.storage = self.firebase.storage()

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
            self.storage.child(f"{self.DJANGO_USER_ID}/{image_name}").put(image_data)

        except Exception as e:
            print(f"Une erreur est survenue: {e}")


if __name__ == "__main__":
    # REALTIME FIREBASE 
    # syncer = RealtimeFirebaseSync()
    # # Planifie l'exécution de la fonction toutes les 10 secondes
    # schedule.every(10).seconds.do(syncer.sync)

    # # Boucle infinie pour exécuter les tâches planifiées
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

    # STORAGE FIREBASE
    syncer = FirebaseStorageSync()

    schedule.every(10).seconds.do(syncer.sync)

    while True:
        schedule.run_pending()
        time.sleep(1)