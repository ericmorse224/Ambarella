import os
import json
import requests
import logging
from datetime import datetime, timedelta
from pathlib import Path
from app.utils.logger import logger

# Load secrets
SECRETS_FILE = Path.home() / ".app_secrets" / "env.json"
with open(SECRETS_FILE) as f:
    secrets = json.load(f)

ZOHO_CLIENT_ID = secrets["ZOHO_CLIENT_ID"]
ZOHO_CLIENT_SECRET = secrets["ZOHO_CLIENT_SECRET"]
ZOHO_REFRESH_TOKEN = secrets["ZOHO_REFRESH_TOKEN"]

TOKENS_FILE = Path.home() / ".app_secrets" / "zoho_tokens.json"
API_BASE_URL = "https://www.zohoapis.com"

# ========== TOKEN MANAGEMENT ==========

def save_tokens(tokens):
    with open(TOKENS_FILE, "w") as f:
        json.dump(tokens, f, indent=2)
    try:
        TOKENS_FILE.chmod(0o600)
    except Exception as e:
        logger.warning(f"Failed to set permissions on token file: {e}")

def load_tokens():
    if TOKENS_FILE.exists():
        with open(TOKENS_FILE) as f:
            return json.load(f)
    return {}

def refresh_access_token():
    logger.info("Refreshing Zoho access token...")
    response = requests.post("https://accounts.zoho.com/oauth/v2/token", params={
        "refresh_token": ZOHO_REFRESH_TOKEN,
        "client_id": ZOHO_CLIENT_ID,
        "client_secret": ZOHO_CLIENT_SECRET,
        "grant_type": "refresh_token"
    })

    if not response.ok:
        raise Exception(f"Failed to refresh Zoho access token: {response.text}")

    tokens = response.json()
    tokens["refresh_token"] = ZOHO_REFRESH_TOKEN
    save_tokens(tokens)
    return tokens["access_token"]

def load_access_token():
    tokens = load_tokens()
    return tokens.get("access_token") or refresh_access_token()

# ========== GENERIC AUTHORIZED REQUEST WRAPPER ==========

def make_authorized_request(endpoint, method="GET", payload=None):
    access_token = load_access_token()
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        "Content-Type": "application/json"
    }

    url = f"{API_BASE_URL}{endpoint}"
    response = requests.request(method, url, headers=headers, json=payload)

    if response.status_code == 401:
        logger.warning("Access token expired. Refreshing...")
        access_token = refresh_access_token()
        headers["Authorization"] = f"Zoho-oauthtoken {access_token}"
        response = requests.request(method, url, headers=headers, json=payload)

    return response

# ========== CALENDAR FUNCTIONS ==========

def create_calendar_event(title, description, start_time, end_time):
    endpoint = "/calendar/v2/calendars/primary/events"
    payload = {
        "event_title": title,
        "location": "",
        "description": description,
        "all_day": False,
        "start_time": start_time,
        "end_time": end_time,
        "timezone": "UTC"
    }

    response = make_authorized_request(endpoint, method="POST", payload=payload)
    if not response.ok:
        raise Exception(f"Zoho calendar event creation failed: {response.text}")

    return response.json()

def get_user_profile():
    access_token = load_access_token()
    if not access_token:
        access_token = refresh_access_token()

    url = "https://www.zohoapis.com/calendar/v2/users/me"
    headers = {"Authorization": f"Zoho-oauthtoken {access_token}"}
    res = requests.get(url, headers=headers)

    if res.status_code == 401:
        access_token = refresh_access_token()
        headers = {"Authorization": f"Zoho-oauthtoken {access_token}"}
        res = requests.get(url, headers=headers)

    if not res.ok:
        raise Exception(f"Zoho user info failed: {res.text}")

    return res.json()

# ========== MEETING FUNCTIONS ==========

def create_meeting(title, agenda, start_time):
    endpoint = "/meeting/v1/meetings"
    payload = {
        "topic": title,
        "agenda": agenda,
        "start_time": start_time,
        "duration": 30,
        "timezone": "America/New_York"
    }

    response = make_authorized_request(endpoint, method="POST", payload=payload)
    if response.ok:
        logger.info("✅ Zoho Meeting created.")
        return response.json()
    else:
        logger.error(f"❌ Failed to create meeting: {response.text}")
        return None
