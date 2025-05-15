import json
import requests
from pathlib import Path
from flask import jsonify

SECRETS_PATH = Path(__file__).parent / "env.json"
TOKENS_FILE = Path(__file__).parent / "zoho_tokens.json"


def load_tokens():
    if TOKENS_FILE.exists():
        with open(TOKENS_FILE) as f:
            return json.load(f)
    return {}


def refresh_access_token():
    with open(SECRETS_PATH) as f:
        secrets = json.load(f)

    refresh_token = secrets["ZOHO_REFRESH_TOKEN"]
    client_id = secrets["ZOHO_CLIENT_ID"]
    client_secret = secrets["ZOHO_CLIENT_SECRET"]

    response = requests.post("https://accounts.zoho.com/oauth/v2/token", params={
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token"
    })

    if response.ok:
        tokens = response.json()
        tokens["refresh_token"] = refresh_token  # preserve refresh token
        with open(TOKENS_FILE, "w") as f:
            json.dump(tokens, f, indent=2)
        return tokens["access_token"]
    else:
        raise Exception(f"Failed to refresh Zoho access token: {response.text}")


def update_meeting(meeting_key, access_token, payload):
    url = f"https://meeting.zoho.com/api/v1/meetings/{meeting_key}"
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.put(url, headers=headers, json=payload)
    if response.ok:
        return response.json()
    else:
        raise Exception(f"Failed to update meeting: {response.text}")

