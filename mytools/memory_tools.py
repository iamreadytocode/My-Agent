from database.db_client import get_db
from database.vector_db import get_vector_db
from database.sqlite_db import log_message, get_recent_messages
from typing import List, Dict
from langchain_core.tools import tool
import uuid

from datetime import datetime

from google.cloud import firestore

db = get_db()
vector_db = get_vector_db()
my_user_id = "master_admin"

@tool
def save_user_metric(key: str, value: str):
    """Save user metrics like weight, height, goals."""
    db.collection("users").document(my_user_id).set({
    key: value}, merge=True)
    return f"{key} updated to {value}"

@tool
def get_user_profile():
    """Fetch user profile from Firestore."""
    doc = db.collection("users").document(my_user_id).get()
    return doc.to_dict()

# ... (keep your existing imports like db, my_user_id, etc.)

@tool
def record_meal(meal_description: str): 
    """
    Logs a meal or multiple food items to the database.
    Input should be a text description like "chicken sandwich and an apple".
    """
    
    # 1. We handle the "list" logic inside Python, not the API
    # This prevents the 'missing field' error completely.
    # We treat the whole input as one entry for the Vector DB context.
    
    # Add to Firestore
    db.collection("meals").add({
        "user_id": my_user_id,
        "meal": meal_description, 
        "timestamp": firestore.SERVER_TIMESTAMP
    })

    # Add to Vector DB (Chroma)
    vector_db.add(
        documents=[meal_description], 
        metadatas=[{
            "user_id": my_user_id, 
            "type": "meal",
            "date": datetime.now().isoformat()
        }],
        ids=[str(uuid.uuid4())]
    )

    return f"Logged meal: {meal_description}"

@tool
def record_workout(workout: str):
    """Log workout."""

    db.collection("workouts").add({
        "user_id": my_user_id,
        "workout": workout,
        "timestamp": firestore.SERVER_TIMESTAMP   # IMPORTANT
    })
    vector_db.add(
    documents=[workout],
    metadatas=[{
        "user_id": my_user_id,
        "type": "workout"
    }],
    ids=[str(uuid.uuid4())]
    )


    return "Workout logged."


@tool
def search_memory(query: str):
    """Search semantic memory."""
    results = vector_db.query(
    query_texts=[query],
    n_results=5,
    where={"user_id": my_user_id}
)

    return results["documents"]

from google.cloud import firestore
# ... imports ...

@tool
def get_last_meal():
    """Get the most recent logged meal."""
    docs = (
        db.collection("meals")
        .where("user_id", "==", my_user_id)
        .order_by("timestamp", direction=firestore.Query.DESCENDING) # <--- ADDED THIS
        .limit(1)
        .get()
    )

    for d in docs:
        return d.to_dict()

    return "No previous meals found."

@tool
def get_last_workout():
    """Get the most recent logged workout."""
    docs = (
        db.collection("workouts")
        .where("user_id", "==", my_user_id)
        .order_by("timestamp", direction=firestore.Query.DESCENDING) # <--- ADDED THIS
        .limit(1)
        .get()
    )

    for d in docs:
        return d.to_dict()

    return "No previous workouts found."

@tool
def log_note(note: str):
    """Log a general memory note."""
    db.collection("notes").add({
        "user_id": my_user_id,
        "note": note,
        "timestamp": firestore.SERVER_TIMESTAMP
    })

    vector_db.add(
        documents=[note],
        metadatas=[{"user_id": my_user_id, "type": "note"}],
        ids=[str(uuid.uuid4())]
    )

    return "Note saved."

def is_duplicate(text: str):
    results = vector_db.query(query_texts=[text], n_results=1)
    return results["distances"][0][0] < 0.1

