from database.db_client import get_db
from database.models import create_user_schema

def initialize_master_user():
    print("--- VIKI User Initialization ---")
    
    # Connect to DB
    try:
        db = get_db()
        print("Database connected.")
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    # Define master user
    user_id = "master_admin"
    name = "VIKI Developer" 
    email = "admin@viki.local"
    
    # Create data structure using schema
    user_data = create_user_schema(user_id, name, email)

    # 4. Save to firestore in 'users'
    db.collection("users").document(user_id).set(user_data)
    
    print(f"User '{name}' created successfully in the 'users' collection.")
    print("VIKI knows who I am.")

if __name__ == "__main__":
    initialize_master_user()