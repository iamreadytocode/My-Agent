import sqlite3
import os
from datetime import datetime

# --- CONFIGURATION ---
# This creates a single file named 'viki_chat.db' in your project folder
DB_PATH = os.path.join(os.getcwd(), "viki_chat.db")

def get_history_db():
    """
    Connects to the local SQLite database for chat history.
    """
    conn = sqlite3.connect(DB_PATH)
    # This allows us to access columns by name (row['message']) instead of index
    conn.row_factory = sqlite3.Row
    return conn

def init_history_db():
    """
    Creates the table if it doesn't exist.
    """
    conn = get_history_db()
    cursor = conn.cursor()
    
    # Create a simple table to store messages
    # Session_ID allows us to keep different conversations separate
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS message_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"✅ Short-term Memory (SQLite) initialized at: {DB_PATH}")

def log_message(session_id, role, content):
    """
    Saves a single message to the history.
    Role = 'user' or 'assistant'
    """
    conn = get_history_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO message_history (session_id, role, content) VALUES (?, ?, ?)",
        (session_id, role, content)
    )
    conn.commit()
    conn.close()

def get_recent_messages(session_id, limit=10):
    """
    Retrieves the last X messages so VIKI knows the context.
    """
    conn = get_history_db()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT role, content FROM message_history WHERE session_id = ? ORDER BY id DESC LIMIT ?",
        (session_id, limit)
    )
    
    rows = cursor.fetchall()
    conn.close()
    
    # Reverse them so they are in chronological order (Oldest -> Newest)
    return [{"role": row["role"], "content": row["content"]} for row in reversed(rows)]

# --- TEST BLOCK ---
if __name__ == "__main__":
    # 1. Initialize the table
    init_history_db()
    
    # 2. Simulate a conversation
    test_session = "test_session_001"
    log_message(test_session, "user", "Hi VIKI, who am I?")
    log_message(test_session, "assistant", "You are the Master Admin.")
    
    # 3. Retrieve it to prove memory works
    history = get_recent_messages(test_session)
    print("--- Recent Chat History ---")
    for msg in history:
        print(f"{msg['role']}: {msg['content']}")