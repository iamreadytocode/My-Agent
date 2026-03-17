
from langchain_core.tools import tool
from mytools.memory_tools import save_user_metric
import requests

import requests
import os

def get_icd_token():
    url = "https://icdaccessmanagement.who.int/connect/token"

    payload = {
        "client_id": os.getenv("ICD_CLIENT_ID"),
        "client_secret": os.getenv("ICD_CLIENT_SECRET"),
        "grant_type": "client_credentials",
        "scope": "icdapi_access"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=payload, headers=headers)

    return response.json()["access_token"]

@tool("health_lookup")
def health_lookup(symptom: str):
    """Lookup health info from WHO ICD API."""
    token = get_icd_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    url = f"https://id.who.int/icd/release/11/2023-01/mms/search?q={symptom}"

    r = requests.get(url, headers=headers)

    return r.text


@tool
def log_symptom(user_id: str, symptom: str):
    """Store reported symptom."""
    save_user_metric(user_id, "last_symptom", symptom)
    return "Symptom logged."


@tool
def explain_health_topic(topic: str):
    """Explain health topic simply."""
    return f"{topic} is related to hormonal or immune system balance."
