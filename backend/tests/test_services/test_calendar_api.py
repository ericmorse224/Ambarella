import pytest
from unittest.mock import patch, Mock
from app.services.calendar_api import create_calendar_event, create_event_payload, make_authorized_request
import datetime

def test_create_event_payload_date_objects():
    start = datetime.datetime(2025, 1, 1, 9, 0)
    end = datetime.datetime(2025, 1, 1, 10, 0)
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

@patch("app.services.calendar_api.make_authorized_request")
def test_create_calendar_event_invalid_response_type(mock_request):
    mock_request.return_value = "unexpected string"
    with pytest.raises(Exception):
        create_calendar_event("Alice", "String Response", "2025-06-01T10:00:00", "2025-06-01T10:30:00")

@patch("app.services.calendar_api.make_authorized_request")
def test_create_calendar_event_json_error(mock_request):
    mock_response = Mock()
    mock_response.json.side_effect = ValueError("Invalid JSON")
    mock_request.return_value = mock_response

    with pytest.raises(Exception, match="Zoho calendar event creation failed"):
        create_calendar_event("Bob", "Do something", "2025-06-01T10:00", "2025-06-01T10:30")

@patch("app.services.calendar_api.make_authorized_request", side_effect=Exception("Zoho calendar event creation failed: mock error"))
def test_create_calendar_event_failure(mock_request):
    with pytest.raises(Exception) as excinfo:
        create_calendar_event("Bob", "Fail case", "2025-05-21T15:00:00", "2025-05-21T15:30:00")
    assert "Zoho calendar event creation failed" in str(excinfo.value)

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

@patch("app.services.calendar_api.make_authorized_request", side_effect=Exception("Network down"))
def test_create_calendar_event_network_error(mock_request):
    with pytest.raises(Exception) as excinfo:
        create_calendar_event("Alice", "Outage recovery", "2025-05-22T09:00:00", "2025-05-22T09:30:00")
    assert "Network down" in str(excinfo.value)

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

@patch("app.services.calendar_api.make_authorized_request", side_effect=Exception("Network down"))
def test_create_calendar_event_network_error(mock_request):
    with pytest.raises(Exception) as excinfo:
        create_calendar_event("Bob", "Submit report", "2025-05-21T15:00:00", "2025-05-21T15:30:00")
    assert "Network down" in str(excinfo.value)

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

@patch("app.services.calendar_api.make_authorized_request")
def test_create_calendar_event_returns_dict(mock_request):
    mock_response = Mock()
    mock_response.ok = True
    mock_response.json.return_value = {"result": "success"}
    mock_request.return_value = mock_response

    result = create_calendar_event("Alice", "Discuss roadmap", "2025-06-01T09:00", "2025-06-01T09:30")
    assert result == {"result": "success"}


@patch("app.services.calendar_api.make_authorized_request")
def test_create_calendar_event_empty_response(mock_request):
    mock_response = Mock()
    mock_response.ok = False
    mock_request.return_value = mock_response

    with pytest.raises(Exception) as excinfo:
        create_calendar_event("Bob", "Empty case", "2025-06-01T10:00", "2025-06-01T10:30")
    assert "Zoho calendar event creation failed" in str(excinfo.value)

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

@patch("app.services.calendar_api.make_authorized_request")
def test_create_calendar_event_success_mocked(mock_request):
    mock_response = Mock()
    mock_response.ok = True
    mock_response.json.return_value = {"status": "created"}
    mock_request.return_value = mock_response

    result = create_calendar_event("Eve", "Demo", "2025-06-02T14:00", "2025-06-02T14:30")
    assert result == {"status": "created"}

@patch("app.services.calendar_api.make_authorized_request")
def test_create_calendar_event_handles_non_dict_response(mock_request):
    mock_request.return_value = None
    with pytest.raises(Exception):
        create_calendar_event("Alice", "Discuss roadmap", "2025-06-01T10:00:00", "2025-06-01T10:30:00")