import sys
import os
from datetime import datetime, timedelta, timezone
# Add project base directory to sys.path to ensure all imports work correctly
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pytest
from caldav import DAVClient
import json
from app.services.calendar_api import create_calendar_event, create_event_payload
from tests.test_services.test_nextcloud_client import get_nextcloud_client

def test_create_event_payload_date_objects():
    start = datetime(2025, 1, 1, 9, 0)
    end = datetime(2025, 1, 1, 10, 0)
    payload = create_event_payload("Bob", "Discuss plan", start, end)
    assert payload["start_time"] == str(start)
    assert payload["end_time"] == str(end)

def test_create_event_payload_mixed_input_types():
    payload = create_event_payload(999, ["Plan"], {"start": "9"}, None)
    assert payload["title"] == "Meeting with 999"
    assert payload["agenda"] == "['Plan']"
    assert payload["start_time"] == "{'start': '9'}"
    assert payload["end_time"] == ""

def test_create_event_payload_attendee_formatting():
    payload = create_event_payload("John", "Agenda", "Start", "End")
    assert isinstance(payload["attendees"], list)
    assert isinstance(payload["attendees"][0], dict)
    assert payload["attendees"][0]["name"] == "John"

def test_create_event_payload_handles_tuple_input():
    payload = create_event_payload(("Jane",), ("Task",), ("2025-01-01",), ("2025-01-02",))
    assert payload["title"] == "Meeting with ('Jane',)"
    assert payload["agenda"] == "('Task',)"
    assert payload["start_time"] == "('2025-01-01',)"
    assert payload["end_time"] == "('2025-01-02',)"

def test_create_event_payload_dict_input():
    payload = create_event_payload({"name": "Eva"}, {"action": "present"}, {}, {})
    assert payload["title"] == "Meeting with {'name': 'Eva'}"
    assert payload["agenda"] == "{'action': 'present'}"
    assert payload["start_time"] == "{}"
    assert payload["end_time"] == "{}"

def test_create_event_payload_structure():
    payload = create_event_payload("Alice", "Submit report", "2025-05-21T10:00:00", "2025-05-21T10:30:00")
    assert payload["title"] == "Meeting with Alice"
    assert payload["agenda"] == "Submit report"
    assert payload["start_time"] == "2025-05-21T10:00:00"
    assert payload["end_time"] == "2025-05-21T10:30:00"
    assert payload["attendees"] == [{"name": "Alice"}]

def test_create_event_payload_with_empty_owner():
    payload = create_event_payload("", "Submit report", "2025-05-21T10:00:00", "2025-05-21T10:30:00")
    assert payload["attendees"] == [{"name": "Unassigned"}]
    assert payload["title"] == "Meeting with Unassigned"

def test_create_event_payload_missing_action():
    payload = create_event_payload("Bob", "", "2025-05-21T10:00:00", "2025-05-21T10:30:00")
    assert payload["title"] == "Meeting with Bob"
    assert payload["agenda"] == ""

def test_create_event_payload_none_values():
    payload = create_event_payload(None, None, None, None)
    assert payload["title"] == "Meeting with Unassigned"
    assert payload["agenda"] == ""
    assert payload["start_time"] == ""
    assert payload["end_time"] == ""
    assert payload["attendees"] == [{"name": "Unassigned"}]

def test_create_event_payload_special_chars():
    payload = create_event_payload("🚀", "Discuss Q2 📊", "2025-05-20T11:00:00", "2025-05-20T11:30:00")
    assert "🚀" in payload["title"]
    assert "📊" in payload["agenda"]

def test_create_event_payload_long_names():
    long_name = "A" * 300
    payload = create_event_payload(long_name, "Annual review", "2025-05-21T12:00:00", "2025-05-21T12:30:00")
    assert payload["attendees"][0]["name"] == long_name
    assert payload["title"] == f"Meeting with {long_name}"

def test_create_event_payload_numeric_inputs():
    payload = create_event_payload(123, 456, 789, 101112)
    assert payload["title"] == "Meeting with 123"
    assert payload["agenda"] == "456"
    assert payload["start_time"] == "789"
    assert payload["end_time"] == "101112"
    assert payload["attendees"] == [{"name": "123"}]

def test_create_event_payload_boolean_inputs():
    payload = create_event_payload(True, False, True, False)
    assert payload["title"] == "Meeting with True"
    assert payload["agenda"] == "False"
    assert payload["start_time"] == "True"
    assert payload["end_time"] == "False"
    assert payload["attendees"] == [{"name": "True"}]

def test_create_event_payload_list_inputs():
    payload = create_event_payload(["Alice"], ["Agenda"], ["2025-01-01T09:00:00"], ["2025-01-01T10:00:00"])
    assert payload["title"] == "Meeting with ['Alice']"
    assert payload["agenda"] == "['Agenda']"
    assert payload["attendees"] == [{"name": "['Alice']"}]

def test_create_event_payload_empty_strings():
    payload = create_event_payload("", "", "", "")
    assert payload["title"] == "Meeting with Unassigned"
    assert payload["agenda"] == ""
    assert payload["start_time"] == ""
    assert payload["end_time"] == ""
    assert payload["attendees"] == [{"name": "Unassigned"}]

def test_create_event_payload_special_input_types():
    class Dummy:
        def __str__(self):
            return "DummyObject"
    dummy = Dummy()
    payload = create_event_payload(dummy, dummy, dummy, dummy)
    assert payload["title"] == "Meeting with DummyObject"
    assert payload["agenda"] == "DummyObject"
    assert payload["attendees"] == [{"name": "DummyObject"}]

def test_create_event_payload_whitespace_inputs():
    payload = create_event_payload("   ", "   ", "   ", "   ")
    assert payload["title"] == "Meeting with Unassigned"
    assert payload["agenda"] == ""
    assert payload["start_time"] == ""
    assert payload["end_time"] == ""
    assert payload["attendees"] == [{"name": "Unassigned"}]

def test_create_event_payload_html_injection():
    payload = create_event_payload("<script>", "<b>Important</b>", "<div>", "<div>")
    assert payload["title"] == "Meeting with <script>"
    assert payload["agenda"] == "<b>Important</b>"

def test_create_event_payload_long_inputs():
    long_name = "A" * 1000
    payload = create_event_payload(long_name, long_name, long_name, long_name)
    assert payload["title"] == f"Meeting with {long_name}"
    assert payload["agenda"] == long_name
    assert payload["start_time"] == long_name
    assert payload["end_time"] == long_name

def test_create_event_payload_structure_valid():
    payload = create_event_payload("Eve", "Demo", "2025-06-02T14:00", "2025-06-02T14:30")
    assert payload["title"].startswith("Meeting with")
    assert isinstance(payload, dict)
    assert isinstance(payload.get("attendees"), list)

@pytest.mark.skip("Will test later")
def test_create_calendar_event_nextcloud_success():
    # This will create a real event in Nextcloud.
    # Set up your test Nextcloud with valid secrets for this to pass!
    title = "Test Meeting"
    description = "Automated test event"
    start = "2025-06-05T09:00:00"
    end = "2025-06-05T09:30:00"
    result = create_calendar_event(title, description, start, end)
    print("\nResult from create_calendar_event:", result)

    assert result is not None, "create_calendar_event returned None"
    assert isinstance(result, (str, dict))  # Adjust as per your real function's return type

@pytest.mark.skip("No longer auto-scheduling")
def test_create_calendar_event_and_verify_in_nextcloud():
    title = "Pytest Meeting"
    description = "Automated test event from pytest"
    start = (datetime.fromisoformat(datetime.now(timezone.utc)) + timedelta(hours=2)).isoformat()
    #dt1 = datetime.now(timezone.utc) + timedelta(hours=2)
    #start = datetime.strptime(str(dt1),"%Y-%m-%d %H:%M:%S.%f%z")
    #start_formatted = dt1.isoformat()
    #start = start_formatted[:16]
    #start = dt1.strftime('%Y-%m-%dT%H:%M')
    end = (datetime.fromisoformat(datetime.now(timezone.utc)) + timedelta(hours=3)).isoformat()
    #dt2 = datetime.now(timezone.utc) + timedelta(hours=2, minutes=30)
    #end = datetime.strptime(str(dt2),"%Y-%m-%d %H:%M:%S.%f%z")
    #end_formatted = end.isoformat()
    #end = end_formatted[:16]
    #end = dt2.strftime('%Y-%m-%dT%H:%M')
    create_calendar_event(title, description, start, end)

    client = get_nextcloud_client()
    principal = client.principal()
    calendars = principal.calendars()
    assert calendars, "No calendars found in Nextcloud"
    calendar = calendars[0]

    events = list(calendar.events())
    found = any(title in event.data and start[:16] in event.data for event in events)
    assert found, f"Event with title '{title}' and start '{start}' not found in Nextcloud calendar!"