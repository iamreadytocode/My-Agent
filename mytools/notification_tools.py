from plyer import notification
from langchain_core.tools import tool

@tool
def send_notification(title: str, message: str):
    """Sends a desktop notification."""
    notification.notify(
        title=title,
        message=message,
        timeout=10
    )
    return "Notification sent."