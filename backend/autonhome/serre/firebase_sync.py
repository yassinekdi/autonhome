import os
import requests
import pyrebase
from dotenv import load_dotenv
from pytz import timezone
from datetime import datetime
from constants import europe_paris_timezone, temperature_sensor_id, humidity_sensor_id

# Charge les variables d'environnement
load_dotenv()

class FirebaseSync:

    def __init__(self,timezone_area=europe_paris_timezone):
        """
        Initialize FirebaseSync with environment variables
        """
        self.FIREBASE_HOST = os.getenv("FIREBASE_HOST")
        self.FIREBASE_AUTH = os.getenv("FIREBASE_AUTH")
        self.DJANGO_API = os.getenv("DJANGO_API")
        self.DJANGO_USERNAME = os.getenv("DJANGO_USERNAME")
        self.DJANGO_PASSWORD = os.getenv("DJANGO_PASSWORD")
        self.timezone=timezone(timezone_area)

        self.config = {
            "apiKey": self.FIREBASE_AUTH,
            "authDomain": "autonhome-af7ba.firebaseapp.com",
            "databaseURL": self.FIREBASE_HOST,
            "storageBucket": "autonhome-af7ba.appspot.com",
        }


        self.firebase = pyrebase.initialize_app(self.config)
        self.db = self.firebase.database()

    def get_auth_token(self):
        """
        Authenticate with Django API and get JWT token
        """
        response = requests.post("http://localhost:8000/api/token/", data={"username": self.DJANGO_USERNAME, "password": self.DJANGO_PASSWORD})
        return response.json()["access"]

    def fetch_data_from_firebase(self,node="air_monitoring"):
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
    
    def process_firebase_data(self,firebase_measure):
        """
        Process a single measure from Firebase, converting it into the data format
        required by the Django API.
        """
        timestamp_int = firebase_measure.val()['timestamp']  
        timestamp = self.convert_timestamp(timestamp_int) 
        
        return [
                    {
                        "sensor": temperature_sensor_id, 
                        "value": firebase_measure.val()["temperature"],
                        "timestamp": timestamp.isoformat()
                    },
                    {
                        "sensor": humidity_sensor_id,
                        "value": firebase_measure.val()["humidity"],
                        "timestamp": timestamp.isoformat()
                    }
                ]
    
    def create_Measure(self,data,headers):
        """
        Send a POST request to the Django API to create a new Measure instance.
        """
        response = requests.post(self.DJANGO_API, json=data, headers=headers)
        print(response.status_code, response.json())
        
    def sync_firebase_data(self):
        """
        Fetch data from Firebase, process it and create new Measure instances
        in the
        """
        try:
            node="air_monitoring"
            firebase_data = self.fetch_data_from_firebase(node)

            for measure in firebase_data['measures'].each():                
                data = self.process_firebase_data(measure)                
                for measure_data in data:              
                    self.create_Measure(measure_data, firebase_data['headers']) # Send post request to API to create Measure instance.
            
                
        except Exception as e:
            print(' ')
            print(f"Une erreur s'est produite lors de la synchronisation des données: {e}")


if __name__ == "__main__":
    # If this script is run directly, create a FirebaseSync instance and sync data.
    syncer = FirebaseSync()
    syncer.sync_firebase_data()
