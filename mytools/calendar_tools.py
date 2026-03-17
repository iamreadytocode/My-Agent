import os.path
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from langchain_core.tools import tool

# --- AUTH SETUP ---
SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/tasks",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.compose"
]

TOKEN_FILE = "token.pickle"
CREDENTIALS_FILE = "credentials.json"
MY_TIMEZONE = 'Asia/Karachi'
TIMEZONE_OFFSET = "+05:00" # Sargodha timezone offset

def get_services():
    """Authenticates and returns both Calendar and Task services."""
    creds = None
    
    # 1. Correctly load the Pickle token
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, "rb") as token:
                creds = pickle.load(token)
        except Exception:
            creds = None

    # 2. If invalid or missing, log in again
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save correctly as a .pickle file
        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)

    return (
        build("calendar", "v3", credentials=creds),
        build("tasks", "v1", credentials=creds)
    )

# --- TOOLS ---

@tool
def create_event(summary: str, start_time: str, end_time: str):
    """
    Create calendar event. 
    Input format: ISO timestamps (e.g., '2026-02-21T18:00:00')
    """
    calendar_service, _ = get_services()

    event = {
        "summary": summary,
        "start": {"dateTime": start_time, "timeZone": MY_TIMEZONE},
        "end": {"dateTime": end_time, "timeZone": MY_TIMEZONE},
    }

    try:
        created = calendar_service.events().insert(
            calendarId="primary",
            body=event
        ).execute()
        return f"Event created successfully: {created.get('htmlLink')}"
    except Exception as e:
        return f"Error creating event: {str(e)}"

@tool
def list_events_on_date(target_date: str):
    """
    List events for a specific date to find their IDs.
    Input format: 'YYYY-MM-DD' (e.g., '2026-02-21').
    """
    calendar_service, _ = get_services()
    
    # Use the correct timezone offset instead of Z (UTC)
    start_of_day = f"{target_date}T00:00:00{TIMEZONE_OFFSET}"
    end_of_day = f"{target_date}T23:59:59{TIMEZONE_OFFSET}"

    events = calendar_service.events().list(
        calendarId="primary",
        timeMin=start_of_day,
        timeMax=end_of_day,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    items = events.get("items", [])
    
    if not items:
        return f"No events found on {target_date}."

    result_str = f"Events on {target_date}:\n"
    for e in items:
        start = e['start'].get('dateTime', e['start'].get('date'))
        result_str += f"- ID: {e['id']} | Summary: {e['summary']} | Time: {start}\n"
    
    return result_str

@tool
def create_task(title: str):
    """Create Google Task."""
    _, tasks_service = get_services()
    task = {"title": title}
    try:
        result = tasks_service.tasks().insert(
            tasklist="@default",
            body=task
        ).execute()
        return f"Task created: {result['title']}"
    except Exception as e:
        return f"Error creating task: {str(e)}"

@tool
def reschedule_event(event_id: str, new_start_time: str, new_end_time: str):
    """
    Move an existing event to a new time.
    Requires event_id from list_events_on_date.
    """
    calendar_service, _ = get_services()

    try:
        event = calendar_service.events().get(calendarId='primary', eventId=event_id).execute()
        
        event['start'] = {'dateTime': new_start_time, 'timeZone': MY_TIMEZONE}
        event['end'] = {'dateTime': new_end_time, 'timeZone': MY_TIMEZONE}

        updated_event = calendar_service.events().update(
            calendarId='primary',
            eventId=event_id,
            body=event
        ).execute()

        return f"Event moved to {new_start_time}: {updated_event['htmlLink']}"
    except Exception as e:
        return f"Error rescheduling event: {str(e)}"

@tool
def delete_event(event_id: str):
    """Remove an event from the calendar."""
    calendar_service, _ = get_services()
    try:
        calendar_service.events().delete(
            calendarId='primary',
            eventId=event_id
        ).execute()
        return "Event successfully deleted."
    except Exception as e:
        return f"Error deleting event: {str(e)}"