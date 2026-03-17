
import firebase_admin
from firebase_admin import credentials, firestore
from database.models import create_user_schema

# Initialize the Connection
cred = credentials.Certificate("path/to/your/serviceAccountKey.json") 
firebase_admin.initialize_app(cred)

db = firestore.client()

def initialize_database(user_id, name, email):
    """
    This function creates the initial collections in Firestore
    based on our models.
    """
    print("... Connecting to Firestore")
    
    # Create reference to 'users'
    user_ref = db.collection("users").document(user_id)
    
    # Get blueprint
    user_data = create_user_schema(user_id, name, email)
    
    # Save it 
    user_ref.set(user_data)
    
    print(f" Success! User {name} created in Firestore.")

# --- TEST IT ---
if __name__ == "__main__":
    initialize_database("student_01", "Abdullah", "abdullah@example.com")