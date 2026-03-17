import firebase_admin
from firebase_admin import credentials, firestore
import os


CRED_FILE = "service_account.json"
DATABASE_ID = os.getenv("FIRESTORE_DB_ID")  # The specific database ID

def get_db():
    """
    Connects to Firestore and returns the database client.
    Checks if a connection already exists to prevent errors.
    """
    #  Checks if Firebase is running
    if not firebase_admin._apps:
        # If not, initialize it
        if os.path.exists(CRED_FILE):
            cred = credentials.Certificate(CRED_FILE)
            firebase_admin.initialize_app(cred)
        else:
            raise FileNotFoundError(f"ERROR: Could not find {CRED_FILE} in the root folder.")

    # 2. Connect to my  database
    db = firestore.client(database_id=DATABASE_ID)
    
    return db