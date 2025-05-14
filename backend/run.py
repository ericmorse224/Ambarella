from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests
import subprocess
import logging
import time
import nltk
from nltk.tokenize import sent_tokenize
from dotenv import load_dotenv
from datetime import datetime, timedelta
from zoho_utils import create_calendar_event
from calendar_integration import extract_people, assign_actions_to_people, create_calendar_events
from zoho_auth import get_auth_url, exchange_code_for_tokens, zoho_bp
from zoho_utils import get_user_profile 
from llm_utils import generate_summary_and_extraction
import re
from pathlib import Path
import json


nltk.download('punkt')

# Load secrets from ~/.app_secrets/env.json
SECRETS_DIR = Path.home() / ".app_secrets"
SECRETS_PATH = SECRETS_DIR / "env.json"
if not SECRETS_PATH.exists():
    raise FileNotFoundError(f"Missing secrets file: {SECRETS_PATH***REMOVED***")

with open(SECRETS_PATH) as f:
    secrets = json.load(f)

ASSEMBLYAI_API_KEY = secrets["ASSEMBLYAI_API_KEY"]
if not ASSEMBLYAI_API_KEY:
    raise ValueError("Missing ASSEMBLYAI_API_KEY environment variable.")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"***REMOVED******REMOVED***)
app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024
app.register_blueprint(zoho_bp)

# Logging setup
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def log_transcript_to_file(transcript):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs("transcripts", exist_ok=True)
    path = os.path.join("transcripts", f"transcript_{timestamp***REMOVED***.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(transcript)
    logging.info(f"Transcript logged to {path***REMOVED***")

def assign_owner(action, entities, last_mentioned=None):
    person_entities = [e.lower() for e in entities]

    pronouns = {
        "he": last_mentioned,
        "she": last_mentioned,
        "they": last_mentioned
    ***REMOVED***

    lower_action = action.lower()
    is_ambiguous = False

    for person in person_entities:
        if person in lower_action:
            cleaned_action = action.replace(person, '').strip()
            assigned = f"{person.title()***REMOVED*** needs to {cleaned_action***REMOVED***"
            return person.title(), assigned, is_ambiguous

    for pronoun, fallback in pronouns.items():
        if pronoun in lower_action and fallback:
            assigned = f"{fallback.title()***REMOVED*** needs to {action***REMOVED***"
            return fallback.title(), assigned, is_ambiguous

    # Fallback
    assigned = f"Someone needs to {action***REMOVED***"
    is_ambiguous = True

    generic_verbs = ["do", "handle", "fix", "work", "make", "take care", "something"]
    if any(word in lower_action for word in generic_verbs) or len(action.split()) < 3:
        is_ambiguous = True

    return "Someone", assigned, is_ambiguous

@app.route("/auth-url")
def auth_url():
    return jsonify({"url": get_auth_url()***REMOVED***)

@app.route("/callback")
def auth_callback():
    code = request.args.get("code")
    if not code:
        return "Authorization code not found.", 400
    try:
        tokens = exchange_code_for_tokens(code)
        return "Authorization successful."
    except Exception as e:
        return f"Error exchanging code: {e***REMOVED***", 500

@app.route('/process-audio', methods=['POST'])
def process_audio():
    try:
        file = request.files.get('audio')
        if not file or not file.content_type.startswith('audio/'):
            return jsonify({"error": "Invalid file or missing."***REMOVED***), 400

        file.seek(0, os.SEEK_END)
        if file.tell() > 25 * 1024 * 1024:
            return jsonify({"error": "File too large! Max 25MB allowed."***REMOVED***), 400
        file.seek(0)

        original_path = "original_audio.wav"
        converted_path = "converted_audio.wav"
        trimmed_path = "trimmed_audio.wav"
        file.save(original_path)

        subprocess.run(["ffmpeg", "-y", "-i", original_path, "-ac", "1", "-ar", "16000", converted_path], check=True)
        try:
            subprocess.run([
                "ffmpeg", "-y", "-i", converted_path,
                "-af", "silenceremove=start_periods=1:start_duration=0.5:start_threshold=-50dB:stop_periods=1:stop_duration=0.5:stop_threshold=-50dB",
                trimmed_path
            ], check=True)
            final_path = trimmed_path
        except subprocess.CalledProcessError:
            final_path = converted_path

        with open(final_path, 'rb') as f:
            upload_res = requests.post(
                'https://api.assemblyai.com/v2/upload',
                headers={'authorization': ASSEMBLYAI_API_KEY***REMOVED***,
                data=f
            )
        logging.info("Upload response: %s", upload_res.text)
        upload_url = upload_res.json()['upload_url']

        transcript_res = requests.post(
            'https://api.assemblyai.com/v2/transcript',
            headers={'authorization': ASSEMBLYAI_API_KEY, 'content-type': 'application/json'***REMOVED***,
            json={
                'audio_url': upload_url,
                'punctuate': True,
                'entity_detection': True
            ***REMOVED***
        )
        transcript_id = transcript_res.json()['id']

        polling_url = f'https://api.assemblyai.com/v2/transcript/{transcript_id***REMOVED***'
        while True:
            status_res = requests.get(polling_url, headers={'authorization': ASSEMBLYAI_API_KEY***REMOVED***)
            status_data = status_res.json()
            if status_data['status'] == 'completed':
                transcript = status_data['text']
                entities = status_data.get('entities', [])
                log_transcript_to_file(transcript)
                return jsonify({'transcript': transcript, 'entities': entities***REMOVED***)
            elif status_data['status'] == 'error':
                return jsonify({"error": "Transcription failed", "details": status_data.get("error")***REMOVED***), 500
            time.sleep(3)

    except Exception as e:
        logging.exception("Unhandled error in /process-audio")
        return jsonify({"error": "Unexpected server error", "details": str(e)***REMOVED***), 500
    finally:
        for path in ["original_audio.wav", "converted_audio.wav", "trimmed_audio.wav"]:
            if os.path.exists(path):
                os.remove(path)


@app.route('/process-json-for-AB-testing', methods=['POST'])
def process_json_for_AB_testing():
    data = request.get_json()
    transcript = data.get("transcript")
    entities = data.get("entities", [])

    if not transcript:
        return jsonify({"error": "Transcript missing."***REMOVED***), 400

    sentences = sent_tokenize(transcript)
    summary, actions, decisions = [], [], []
    action_keywords = ["will", "must", "should", "needs to", "is responsible for"]

    for sentence in sentences:
        lower = sentence.lower()
        if any(k in lower for k in action_keywords):
            actions.append(sentence)
        elif "decision" in lower or "decided" in lower:
            decisions.append(sentence)
        else:
            summary.append(sentence)

    people = extract_people(transcript)
    assigned_actions = assign_actions_to_people(actions, people)
    create_calendar_events(assigned_actions)

    return jsonify({
        "summary": summary,
        "actions": [a['text'] for a in assigned_actions],
        "decisions": decisions
    ***REMOVED***)

@app.route('/create-event', methods=['POST'])
def create_event():
    data = request.get_json()
    events = data.get("events", [])

    if not events:
        return jsonify({"error": "No events provided"***REMOVED***), 400

    try:
        for event in events:
            title = f"Follow-up: {event['owner']***REMOVED***" if event.get('owner') else "Meeting Follow-up"
            description = f"{event['text']***REMOVED***\n\nOwner: {event.get('owner', 'Unassigned')***REMOVED***"
            start = event["startTime"]
            end = (datetime.fromisoformat(start) + timedelta(minutes=30)).isoformat()

            create_calendar_event(title, description, start, end)

        return jsonify({"success": True***REMOVED***)
    except Exception as e:
        logging.exception("Failed to create events")
        return jsonify({"error": "Failed to create one or more events", "details": str(e)***REMOVED***), 500

@app.route('/zoho/user')
def get_zoho_user():
    try:
        profile = get_user_profile()
        return jsonify(profile)
    except Exception as e:
        return jsonify({"error": str(e)***REMOVED***), 500

def parse_llm_sections(text):
    def extract_section(name):
        pattern = rf"{name***REMOVED***:\s*([\s\S]*?)(?=\n[A-Z][a-z]+:|\Z)"
        match = re.search(pattern, text)
        if match:
            lines = match.group(1).strip().split('\n')
            return [line.strip('-\u2022 ').strip() for line in lines if line.strip()]
        return []

    return {
        "summary": extract_section("Summary"),
        "actions": extract_section("Action Items"),
        "decisions": extract_section("Decisions"),
    ***REMOVED***

@app.route('/process-json', methods=['POST'])
def process_json():
    try:
        data = request.get_json()
        transcript = data.get("transcript", "")
        entities = data.get("entities", [])

        if not transcript:
            return jsonify({"error": "Transcript missing."***REMOVED***), 400

        raw_output = generate_summary_and_extraction(transcript)
        parsed = parse_llm_sections(raw_output)

        assigned_actions = []
        ambiguous_actions = []
        last_mentioned = None
        people = [e['text'] for e in entities if e.get('entity_type') == 'person']

        for action in parsed["actions"]:
            owner, assignment, is_ambiguous = assign_owner(action, people, last_mentioned)
            if owner != "Someone":
                last_mentioned = owner
            if is_ambiguous:
                ambiguous_actions.append(assignment)
            else:
                assigned_actions.append(assignment)

        for a in assigned_actions:
            try:
                start_time = datetime.now() + timedelta(hours=1)
                end_time = start_time + timedelta(minutes=30)
                create_calendar_event("Follow-up", a, start_time.isoformat(), end_time.isoformat())
            except Exception as e:
                print("Calendar error:", e)
        create_calendar_events(actions, entities)
        return jsonify({
            "summary": parsed["summary"],
            "actions": assigned_actions,
            "decisions": parsed["decisions"],
            "raw_output": raw_output,
        ***REMOVED***)
    except Exception as e:
        logging.exception("Error in /process-json")
        return jsonify({"error": str(e)***REMOVED***), 500

if __name__ == '__main__':
    app.run(debug=True)