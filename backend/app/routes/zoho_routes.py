import os
import requests
from flask import Blueprint, redirect, request, jsonify
from urllib.parse import quote
import json
from pathlib import Path
from app.utils.zoho_utils import get_user_profile, create_calendar_event
from app.utils.logger import logger
from datetime import datetime, timedelta

# Load secrets from env.json
SECRETS_PATH = os.path.expanduser("~/.app_secrets/env.json")
with open(SECRETS_PATH, "r") as f:
    secrets = json.load(f)

scope = quote("ZohoMeeting.meeting.ALL")
ZOHO_CLIENT_ID = secrets["ZOHO_CLIENT_ID"]
ZOHO_CLIENT_SECRET = secrets["ZOHO_CLIENT_SECRET"]
ZOHO_REDIRECT_URI = secrets["ZOHO_REDIRECT_URI"]
ZOHO_REFRESH_TOKEN = secrets["ZOHO_REFRESH_TOKEN"]

zoho_bp = Blueprint('zoho', __name__)

# ========== OAuth Utility Functions ==========

def get_auth_url():
    return (
        "https://accounts.zoho.com/oauth/v2/auth?"
        f"scope={scope}"
        f"&client_id={ZOHO_CLIENT_ID}"
        f"&response_type=code"
        f"&access_type=offline"
        f"&redirect_uri={ZOHO_REDIRECT_URI}"
        f"&prompt=consent"
    )

def exchange_code_for_tokens(code):
    token_url = "https://accounts.zoho.com/oauth/v2/token"
    data = {
        'grant_type': 'authorization_code',
        'client_id': ZOHO_CLIENT_ID,
        'client_secret': ZOHO_CLIENT_SECRET,
        'redirect_uri': ZOHO_REDIRECT_URI,
        'code': code
    }
    response = requests.post(token_url, data=data)
    if response.ok:
        return response.json()
    else:
        raise Exception(f"Failed to exchange code: {response.text}")

# ========== Routes ==========

@zoho_bp.route("/zoho/auth")
def zoho_auth():
    return redirect(get_auth_url())

@zoho_bp.route("/zoho/callback")
def zoho_callback():
    code = request.args.get("code")
    token_url = "https://accounts.zoho.com/oauth/v2/token"
    data = {
        'grant_type': 'authorization_code',
        'client_id': ZOHO_CLIENT_ID,
        'client_secret': ZOHO_CLIENT_SECRET,
        'redirect_uri': ZOHO_REDIRECT_URI,
        'code': code
    }
    response = requests.post(token_url, data=data)
    if not response.ok:
        return jsonify({"error": "Failed to exchange code for tokens", "details": response.text}), 500

    tokens = response.json()
    secrets["ZOHO_REFRESH_TOKEN"] = tokens.get("refresh_token")
    with open(SECRETS_PATH, "w") as f:
        json.dump(secrets, f, indent=2)

    return jsonify(tokens)

@zoho_bp.route('/api/zoho-token', methods=['GET'])
def get_zoho_token():
    try:
        response = requests.post("https://accounts.zoho.com/oauth/v2/token", data={
            'client_id': ZOHO_CLIENT_ID,
            'client_secret': ZOHO_CLIENT_SECRET,
            'refresh_token': ZOHO_REFRESH_TOKEN,
            'grant_type': 'refresh_token'
        })
        if response.status_code == 200:
            return jsonify(response.json()), 200
        return jsonify({"error": "Failed to fetch Zoho token", "message": response.text}), 500
    except Exception as e:
        return jsonify({"error": "An error occurred", "message": str(e)}), 500

@zoho_bp.route('/zoho/user', methods=['GET'])
def get_zoho_user():
    try:
        profile = get_user_profile()
        return jsonify(profile)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@zoho_bp.route('/create-event', methods=['POST'])
def create_event():
    data = request.get_json()
    events = data.get("events", [])

    if not events:
        return jsonify({"error": "No events provided"}), 400

    try:
        for event in events:
            title = f"Follow-up: {event['owner']}" if event.get('owner') else "Meeting Follow-up"
            description = f"{event['text']}\n\nOwner: {event.get('owner', 'Unassigned')}"
            start = event["startTime"]
            end = (datetime.fromisoformat(start) + timedelta(minutes=30)).isoformat()

            create_calendar_event(title, description, start, end)

        return jsonify({"success": True})
    except Exception as e:
        logger.exception("Failed to create events")
        return jsonify({"error": "Failed to create one or more events", "details": str(e)}), 500
