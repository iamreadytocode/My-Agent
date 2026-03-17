import base64
import os
import pickle
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from langchain_core.tools import tool

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/tasks",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/contacts.readonly" 
]

# UNIFIED TOKEN FILENAME (Matches Calendar Tools)
TOKEN_FILE = "token.pickle"
CREDENTIALS_FILE = "credentials.json"

def get_credentials():
    """
    Robust credential loader. 
    """
    creds = None
    
    # 1. Try to load existing token
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, "rb") as token:
                creds = pickle.load(token)
        except Exception:
            # If we can't read it, destroy it so we can make a new one
            creds = None
            
    # 2. If no valid token, verify we can log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                # If refresh fails, delete and re-login
                if os.path.exists(TOKEN_FILE):
                    os.remove(TOKEN_FILE)
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
        else:
            # First time login or forced re-login
            if os.path.exists(TOKEN_FILE):
                os.remove(TOKEN_FILE) 
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # 3. Save the new, correct binary token
        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)
            
    return creds

# --- TOOLS ---
@tool
def check_unread_emails(limit: int = 5):
    """
    Checks for unread emails. Returns sender, subject, thread_id, and full message body.
    """
    try:
        creds = get_credentials()
        service = build('gmail', 'v1', credentials=creds)
        
        results = service.users().messages().list(userId='me', q='is:unread', maxResults=limit).execute()
        messages = results.get('messages', [])
        
        if not messages:
            return "No new unread emails."

        email_data = []
        for msg in messages:
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()
            payload = txt.get('payload', {})
            headers = payload.get("headers", [])
            
            subject = "No Subject"
            sender = "Unknown Sender"
            thread_id = msg.get('threadId')
            
            for h in headers:
                if h['name'] == 'Subject': subject = h['value']
                if h['name'] == 'From': sender = h['value']
            
            # Extract the actual body text instead of just the snippet
            body_data = ""
            if 'parts' in payload:
                for part in payload['parts']:
                    if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                        body_data = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                        break
            elif 'body' in payload and 'data' in payload['body']:
                body_data = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
            
            if not body_data:
                body_data = txt.get('snippet', 'No text content readable.')

            email_data.append(
                f"• From: {sender}\n"
                f"  Subject: {subject}\n"
                f"  Thread ID: {thread_id}\n"
                f"  Body: {body_data.strip()}\n"
            )

        return "\n---\n".join(email_data)
    except Exception as e:
        return f"Error checking emails: {str(e)}"
@tool
def send_email(to_email: str, subject: str, body: str, thread_id: str = ""): # <--- Changed to empty string
    """
    Sends an email. 'to_email' must be an actual email address.
    If replying to an existing email, provide the 'thread_id' to keep it in the same conversation.
    """
    try:
        creds = get_credentials()
        service = build('gmail', 'v1', credentials=creds)

        message = MIMEText(body)
        message['to'] = to_email
        message['subject'] = subject 
        
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        body_payload = {'raw': raw}
        
        # Check if thread_id exists and is not an empty string
        if thread_id and thread_id.strip() != "":
            body_payload['threadId'] = thread_id
        
        service.users().messages().send(userId='me', body=body_payload).execute()
        
        if thread_id and thread_id.strip() != "":
            return f"Reply sent successfully to {to_email} in thread {thread_id}"
        return f"New email sent successfully to {to_email}"
        
    except Exception as e:
        return f"Error sending email: {str(e)}"

@tool
def get_contact_email(name_query: str):
    """
    Look up an email address from Google Contacts using a name.
    """
    try:
        # 1. Check what Viki is actually searching for
        print(f"\n[DEBUG] Tool triggered! Viki is searching for: '{name_query}'")
        
        creds = get_credentials()
        service = build('people', 'v1', credentials=creds)

        results = service.people().connections().list(
            resourceName='people/me',
            personFields='names,emailAddresses',
            pageSize=1000
        ).execute()

        connections = results.get('connections', [])
        
        # 2. Check how many contacts Python actually sees
        print(f"[DEBUG] Downloaded {len(connections)} contacts from Google.")

        if not connections:
            return "Your contact list is empty."

        # Strip whitespace and make lowercase for safer matching
        name_query_lower = name_query.lower().strip()

        for person in connections:
            names = person.get('names', [])
            emails = person.get('emailAddresses', [])

            if names:
                display_name = names[0].get('displayName', '').lower()
                
                if name_query_lower in display_name:
                    if emails:
                        found_email = emails[0].get('value')
                        # 3. Success state
                        print(f"[DEBUG] MATCH FOUND! Returning: {found_email} to Viki.")
                        return found_email
                    else:
                        # 4. Partial failure state
                        print(f"[DEBUG] Found '{display_name}', but Google says they have no email!")

        print("[DEBUG] Search loop finished. No matches found.")
        return f"Could not find an email address for '{name_query}'."

    except Exception as e:
        print(f"[DEBUG] CRITICAL API ERROR: {str(e)}")
        return f"Error searching contacts: {str(e)}"