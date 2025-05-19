import sys
import os
import re
import requests
import pytest
from caldav import DAVClient
import json
import time
from datetime import datetime, timedelta, timezone
# Add project base directory to sys.path to ensure all imports work correctly
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from app.utils import nextcloud_utils
from app.services import calendar_integration as ci
from tests.test_services.test_nextcloud_client import get_nextcloud_client
from app.utils.entity_utils import extract_entities

def extract_field(ical, field):
    m = re.search(rf"{field}:(.*)", ical)
    if not m:
        return None
    value = m.group(1).replace("\n ", "").replace("\r\n ", "")
    return value.strip()
def find_event_in_nextcloud(title, start):
    client = get_nextcloud_client()
    principal = client.principal()
    calendars = principal.calendars()
    assert calendars, "No calendars found in Nextcloud"
    calendar = calendars[0]
    events = list(calendar.events())
    for event in events:
        if title in event.data and start[:16] in event.data:
            return True
    return False

def test_extract_event_times_with_valid_date():
    now = datetime.now(timezone.utc) + timedelta(days=1)
    test_text = now.strftime("Tomorrow at %I %p")
    start, end = ci.extract_event_times(test_text)
    assert start.endswith("Z")
    assert end.endswith("Z")

def test_extract_event_times_with_invalid_date():
    start, end = ci.extract_event_times("gibberish")
    assert start.endswith("Z")
    assert end.endswith("Z")

def test_extract_people():
    transcript = "Alice and Bob will handle the budget. Charlie will lead."
    entities = extract_entities(transcript)
    people = ci.extract_people_from_entities(entities)
    print("\nPeople extracted:", people)
    assert "Alice" in people
    assert "Bob" in people
    assert "Charlie" in people

def test_assign_actions_to_people():
    actions = ["Alice will review the notes", "Update the slides", "Bob will present"]
    people = ["Alice", "Bob"]
    result = ci.assign_actions_to_people(actions, people)
    assert result[0]["owner"] == "Alice"
    assert result[1]["owner"] == "Unassigned"
    assert result[2]["owner"] == "Bob"

def test_audio_to_nextcloud_event_integration():
    # Step 1: Upload audio and get transcript/entities
    audio_path = "tests/test_audio/All_Needs.wav"
    backend_url = "http://localhost:5000/process-audio"
    with open(audio_path, "rb") as f:
        files = {'audio': (audio_path, f, 'audio/wav')}
        response = requests.post(backend_url, files=files)
        assert response.ok, f"Audio upload failed: {response.text}"
        data = response.json()
    transcript = data.get("transcript")
    entities = data.get("entities", [])
    assert transcript and len(transcript) > 0, "Transcript missing"

    # Step 2: Analyze transcript for actions (if your NLP pipeline is not run on /process-audio)
    analysis_url = "http://localhost:5000/process-json"
    payload = {"transcript": transcript, "entities": entities}
    analysis_response = requests.post(analysis_url, json=payload)
    assert analysis_response.ok, f"Transcript analysis failed: {analysis_response.text}"
    analysis_data = analysis_response.json()
    actions = analysis_data.get("actions", [])
    assert actions and len(actions) > 0, "No actions extracted"

    # Step 3: Create calendar events using your integration logic
    from app.services import calendar_integration as ci
    ci.create_calendar_events(actions)

    # Step 4: Connect to Nextcloud and verify
    from app.utils import nextcloud_utils
    from caldav import DAVClient
    url, username, password = nextcloud_utils.load_nextcloud_secrets()
    client = DAVClient(url, username=username, password=password)
    calendar = client.principal().calendars()[0]
    events = calendar.events()

    def extract_field(ical, field):
        m = re.search(rf"{field}:(.*)", ical)
        if not m:
            return None
        value = m.group(1).replace("\n ", "").replace("\r\n ", "")
        return value.strip()

    for action in actions:
        owner = action.get("owner", "Unassigned")
        title = f"Follow-up: {owner}" if owner != "Unassigned" else "Meeting Follow-up"
        matched = False
        for event in events:
            summary = extract_field(event.data, "SUMMARY")
            if summary == title:
                matched = True
                break
        assert matched, f"Event '{title}' not found in Nextcloud for action: {action}"

    print("All events from audio file successfully created and verified in Nextcloud.")

def test_create_calendar_events_handles_empty(monkeypatch):
    # Should not raise error for empty input
    ci.create_calendar_events([])

def test_create_calendar_events_handles_error(monkeypatch):
    def bad_create(*a, **kw): raise Exception("Fail!")
    monkeypatch.setattr(ci, "create_calendar_event", bad_create)
    actions = [{"owner": "Alice", "text": "Do thing"}]
    # Should not raise, should just handle error internally
    ci.create_calendar_events(actions)
    # Optionally, assert on log output or an error counter if you have one
