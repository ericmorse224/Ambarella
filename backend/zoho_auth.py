# zoho_auth.py
import os
import requests
from flask import Blueprint, redirect, request
from dotenv import load_dotenv
import json
from pathlib import Path
from urllib.parse import quote

SECRETS_DIR = Path.home() / ".app_secrets"
SECRETS_DIR.mkdir(exist_ok=True)

SECRETS_FILE = Path.home() / ".app_secrets" / "env.json"
with open(SECRETS_FILE) as f:
    secrets = json.load(f)

ZOHO_CLIENT_ID = secrets["ZOHO_CLIENT_ID"]
ZOHO_REDIRECT_URI = secrets["ZOHO_REDIRECT_URI"]
ZOHO_CLIENT_SECRET = secrets["ZOHO_CLIENT_SECRET"]
ZOHO_REFRESH_TOKEN = secrets["ZOHO_REFRESH_TOKEN"]

zoho_bp = Blueprint('zoho', __name__)

def get_auth_url():
    scope = quote("ZohoCalendar.events.ALL")
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
    response = request.post(token_url, data=payload)
    if response.ok:
        return response.json()
    else:
        raise Exception(f"Failed to exchange code: {response.text***REMOVED***")

@zoho_bp.route("/zoho/auth")
def zoho_auth():
    url = (
        f"https://accounts.zoho.com/oauth/v2/auth?"
        f"scope=ZohoCalendar.event.ALL&client_id={CLIENT_ID***REMOVED***"
        f"&response_type=code&access_type=offline&redirect_uri={REDIRECT_URI***REMOVED***"
    )
    return redirect(url)

@zoho_bp.route("/zoho/callback")
def zoho_callback():
    code = request.args.get("code")
    token_url = "https://accounts.zoho.com/oauth/v2/token"
    data = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'code': code
    ***REMOVED***
    response = requests.post(token_url, data=data)

    if response.ok:
        tokens = response.json()
        token_path = Path.home() / ".app_secrets" / "zoho_tokens.json"
        token_path.parent.mkdir(parents=True, exist_ok=True)
        with open(token_path, "w") as f:

            json.dump(tokens, f, indent=2)
        return "Authentication successful. Tokens stored securely."
    else:
        return f"Error retrieving tokens: {response.text***REMOVED***", 400
