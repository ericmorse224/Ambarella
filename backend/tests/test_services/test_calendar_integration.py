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

@pytest.mark.skip("No longer auto-scheduling")
def test_auto_schedule_actions_and_verify_nextcloud():
    now = datetime.now(timezone.utc)
    unique_title = f"Pytest Action {now.isoformat()}"
    actions = [unique_title]
    ci.auto_schedule_actions(actions)
    time.sleep(2)
    start, _ = ci.extract_event_times(unique_title)
    found = find_event_in_nextcloud(unique_title, start)
    assert found, f"Event '{unique_title}' not found in Nextcloud"

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

@pytest.mark.skip("Needs audio and the full process completed")
def test_create_calendar_events_and_verify_nextcloud_from_audio():
    #Prerequisite: Your backend (run.py) must be running locally at http://localhost:5000

    # Use your backend endpoint or process directly
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
    
    analysis_url = "http://localhost:5000/process-json"
    payload = {"transcript": transcript, "entities": entities}
    analysis_response = requests.post(analysis_url, json=payload)
    assert analysis_response.ok, f"Transcript analysis failed: {analysis_response.text}"
    analysis_data = analysis_response.json()
    actions = analysis_data.get("actions", [])
    
    assert actions and len(actions) > 0, "No actions extracted"

    time.sleep(4)
    
    from app.services import calendar_integration as ci

    for action in actions:
        # NEW: Use owner key from the action dict
        owner = action.get("owner", "Unassigned")
        title = f"Follow-up: {owner}" if owner != "Unassigned" else "Meeting Follow-up"
        start = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()[:16]
        found = find_event_in_nextcloud(title, start)
        assert found, f"Event '{title}' not found in Nextcloud for action: {action}"

    print("All events from audio file successfully created and verified in Nextcloud.")