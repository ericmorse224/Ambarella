import requests
import json
from datetime import datetime, timedelta
from pathlib import Path
import logging

# Load secrets from env.json
SECRETS_FILE = Path.home() / ".app_secrets" / "env.json"
with open(SECRETS_FILE) as f:
    secrets = json.load(f)

ZOHO_CLIENT_ID = secrets["ZOHO_CLIENT_ID"]
ZOHO_CLIENT_SECRET = secrets["ZOHO_CLIENT_SECRET"]
ZOHO_REFRESH_TOKEN = secrets["ZOHO_REFRESH_TOKEN"]
TOKENS_FILE = Path.home() / ".app_secrets" / "zoho_tokens.json"


# ========== TOKEN HANDLING ==========

def save_tokens(tokens):
    with open(TOKENS_FILE, "w") as f:
        json.dump(tokens, f, indent=2)
    try:
        TOKENS_FILE.chmod(0o600)
    except Exception as e:
        logging.error(f"Failed to save Zoho token: {e***REMOVED***")


def load_tokens():
    if not TOKENS_FILE.exists():
        return {***REMOVED***
    with open(TOKENS_FILE) as f:
        return json.load(f)


def load_access_token():
    tokens = load_tokens()
    return tokens.get("access_token")


def refresh_access_token():
    url = "https://accounts.zoho.com/oauth/v2/token"
    data = {
        "refresh_token": ZOHO_REFRESH_TOKEN,
        "client_id": ZOHO_CLIENT_ID,
        "client_secret": ZOHO_CLIENT_SECRET,
        "grant_type": "refresh_token",
    ***REMOVED***
    response = requests.post(url, data=data)
    if not response.ok:
        raise Exception("Failed to refresh Zoho access token")

    access_token = response.json()["access_token"]
    tokens = load_tokens()
    tokens["access_token"] = access_token
    save_tokens(tokens)
    return access_token, True


# ========== ZOHO API CALL ==========

def create_calendar_event(title, description, start_time, end_time):
    access_token = load_access_token()
    if not access_token:
        access_token, _ = refresh_access_token()

    url = "https://www.zohoapis.com/calendar/v2/calendars/primary/events"
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token***REMOVED***",
        "Content-Type": "application/json"
    ***REMOVED***
    body = {
        "event_title": title,
        "location": "",
        "description": description,
        "all_day": False,
        "start_time": start_time,
        "end_time": end_time,
        "timezone": "UTC"
    ***REMOVED***

    res = requests.post(url, headers=headers, json=body)
    if res.status_code == 401:
        access_token, _ = refresh_access_token()
        headers["Authorization"] = f"Zoho-oauthtoken {access_token***REMOVED***"
        res = requests.post(url, headers=headers, json=body)

    if not res.ok:
        raise Exception(f"Zoho calendar event creation failed: {res.text***REMOVED***")

    return res.json()


def get_user_profile():
    access_token = load_access_token()
    if not access_token:
        access_token, _ = refresh_access_token()

    url = "https://www.zohoapis.com/calendar/v2/users/me"
    headers = {"Authorization": f"Zoho-oauthtoken {access_token***REMOVED***"***REMOVED***
    res = requests.get(url, headers=headers)
    if res.status_code == 401:
        access_token, _ = refresh_access_token()
        headers = {"Authorization": f"Zoho-oauthtoken {access_token***REMOVED***"***REMOVED***
        res = requests.get(url, headers=headers)

    if not res.ok:
        raise Exception(f"Zoho user info failed: {res.text***REMOVED***")

    return res.json()
