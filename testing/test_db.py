
from database.db_client import get_db

print("--- Testing Database Manager ---")

try:
    # Get database 
    db = get_db()
    
    # verify connection
    db.collection("viki_logs").add({
        "message": "Migration successful. VIKI is now using db_client.py",
        "timestamp": "now"
    })
    
    print("Success! new database manager is working.")

except Exception as e:
    print(f" Error: {e}")