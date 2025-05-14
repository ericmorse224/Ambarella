# zoho_auth.py
import os
import requests
from flask import Blueprint, redirect, request, jsonify
from dotenv import load_dotenv
import json
from pathlib import Path
from urllib.parse import quote

# Load secrets from env.json
SECRETS_PATH = os.path.expanduser("~/.app_secrets/env.json")
with open(SECRETS_PATH, "r") as f:
    secrets = json.load(f)

scope = quote("ZohoMeeting.meeting.ALL")
ZOHO_CLIENT_ID = secrets["ZOHO_CLIENT_ID"]
ZOHO_CLIENT_SECRET = secrets["ZOHO_CLIENT_SECRET"]
ZOHO_REDIRECT_URI = secrets["ZOHO_REDIRECT_URI"]
ZOHO_REFRESH_TOKEN = secrets["ZOHO_REFRESH_TOKEN"]

API_BASE_URL = "https://www.zohoapis.com/meeting/v1"

zoho_bp = Blueprint('zoho', __name__)

def get_auth_url():
    return (
        "https://accounts.zoho.com/oauth/v2/auth?"
        f"scope={scope***REMOVED***"
        f"&client_id={ZOHO_CLIENT_ID***REMOVED***"
        f"&response_type=code"
        f"&access_type=offline"
        f"&redirect_uri={ZOHO_REDIRECT_URI***REMOVED***"
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
    ***REMOVED***
    response = request.post(token_url, data=data)
    if response.ok:
        return response.json()
    else:
        raise Exception(f"Failed to exchange code: {response.text***REMOVED***")

@zoho_bp.route("/zoho/auth")
def zoho_auth():
    url = (
        "https://accounts.zoho.com/oauth/v2/auth?"
        f"scope={scope***REMOVED***&client_id={ZOHO_CLIENT_ID***REMOVED***"
        f"&response_type=code&access_type=offline&redirect_uri={ZOHO_REDIRECT_URI***REMOVED***"
    )
    return redirect(url)


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
    ***REMOVED***
    response = requests.post(token_url, data=data)
    if not response.ok:
        return jsonify({"error": "Failed to exchange code for tokens", "details": response.text***REMOVED***), 500

    tokens = response.json()
     # Save tokens to secrets file
    secrets["ZOHO_REFRESH_TOKEN"] = tokens.get("refresh_token")
    with open(SECRETS_PATH, "w") as f:
        json.dump(secrets, f, indent=2)

    return jsonify(tokens)