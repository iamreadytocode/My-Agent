# mytools/google_auth.py

from google.oauth2.credentials import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/calendar",       # Full access to Calendar
    "https://www.googleapis.com/auth/tasks",          # Full access to Tasks
    "https://www.googleapis.com/auth/gmail.modify",   # Read emails AND mark them as read/unread
    "https://www.googleapis.com/auth/gmail.compose"   # Send new emails
]

def get_credentials():
    return Credentials.from_authorized_user_file("token.json", SCOPES)
