import os
import schedule
import time
from dotenv import load_dotenv
from firebase_sync import sync_firebase_data

# Charge les variables d'environnement
load_dotenv()

SYNC_FREQUENCY = int(os.getenv("SYNC_FREQUENCY"))  # en secondes

# Exécute la fonction de synchronisation toutes les SYNC_FREQUENCY secondes
schedule.every(SYNC_FREQUENCY).seconds.do(sync_firebase_data)

while True:
    schedule.run_pending()
    time.sleep(1)
