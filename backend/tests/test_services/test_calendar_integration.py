import sys
import os

# Add project base directory to sys.path to ensure all imports work correctly
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pytest
from datetime import datetime, timedelta, timezone
from app.services import calendar_integration as ci
from caldav import DAVClient
import json
import time
from tests.test_services.test_nextcloud_client import get_nextcloud_client

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

@pytest.mark.skip("Will test later")
def test_extract_people():
    transcript = "Alice and Bob will handle the budget. Charlie will lead."
    people = ci.extract_people_from_entities(transcript)
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

@pytest.mark.skip("Requires a valid audio file and Whisper for full integration test")
def test_create_calendar_events_and_verify_nextcloud():
    now = datetime.now(timezone.utc)
    actions = [
        {"text": f"Follow up with Alice {now}", "owner": "Alice"},
        {"text": f"General meeting review {now}", "owner": "Unassigned"}
    ]
    ci.create_calendar_events(actions)
    time.sleep(2)
    for action in actions:
        title = f"Follow-up: {action['owner']}" if action['owner'] != "Unassigned" else "Meeting Follow-up"
        start = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()[:16]
        found = find_event_in_nextcloud(title, start)
        assert found, f"Event '{title}' not found in Nextcloud"
