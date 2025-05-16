import pytest
import requests
from unittest.mock import patch, Mock, MagicMock
from app.services.calendar_api import create_calendar_event, create_event_payload

from unittest.mock import Mock

@patch("app.services.calendar_api.make_authorized_request")
def test_create_calendar_event_success(mock_request):
    mock_response = Mock()
    mock_response.ok = True
    mock_response.json.return_value = {"status": "success"}
    mock_request.return_value = mock_response

    result = create_calendar_event("Bob", "Submit report", "2025-05-21T15:00:00", "2025-05-21T15:30:00")
    assert result == {"status": "success"}

@patch("app.services.calendar_api.make_authorized_request", side_effect=Exception("Zoho calendar event creation failed: mock error"))
def test_create_calendar_event_failure(mock_request):
    with pytest.raises(Exception) as excinfo:
        create_calendar_event("Bob", "Fail case", "2025-05-21T15:00:00", "2025-05-21T15:30:00")
    assert "Zoho calendar event creation failed" in str(excinfo.value)

def test_create_event_payload_structure():
    payload = create_event_payload("Alice", "Submit the report", "2025-05-20T10:00:00")
    data = payload["data"]
    assert data["title"] == "Meeting with Alice"
    assert data["agenda"] == "Submit the report"
    assert data["start_time"] == "2025-05-20T10:00:00"


def test_create_event_payload_with_empty_owner():
    payload = create_event_payload("", "Submit the report", "2025-05-20T10:00:00")
    assert payload["data"]["attendees"] == [{"name": "Unassigned"}]

def test_create_event_payload_missing_action():
    payload = create_event_payload("Bob", "", "2025-05-20T10:00:00")
    assert payload["data"]["title"] == "Meeting with Bob"
    assert payload["data"]["agenda"] == "Discussion"

@patch("app.services.calendar_api.make_authorized_request", side_effect=Exception("Network down"))
def test_create_calendar_event_network_error(mock_request):
    with pytest.raises(Exception) as excinfo:
        create_calendar_event("Alice", "Outage recovery", "2025-05-22T09:00:00", "2025-05-22T09:30:00")
    assert "Network down" in str(excinfo.value)
