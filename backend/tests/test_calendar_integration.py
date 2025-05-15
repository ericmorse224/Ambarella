import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta, UTC

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import calendar_integration as ci


@patch("calendar_integration.dateparser.parse")
def test_extract_event_times_with_valid_date(mock_parse):
    mock_time = datetime(2025, 5, 14, 10, 0, tzinfo=UTC)
    mock_parse.return_value = mock_time

    start, end = ci.extract_event_times("Tomorrow at 10 AM")
    expected_start = mock_time.isoformat() + "Z"
    expected_end = (mock_time + timedelta(minutes=30)).isoformat() + "Z"

    assert start == expected_start
    assert end == expected_end

@patch("calendar_integration.dateparser.parse", return_value=None)
def test_extract_event_times_with_invalid_date(mock_parse):
    start, end = ci.extract_event_times("gibberish")
    fallback_start = datetime.now(UTC) + timedelta(hours=1)
    fallback_end = fallback_start + timedelta(minutes=30)

    assert start.endswith("Z")
    assert end.endswith("Z")

@patch("calendar_integration.create_calendar_event")
@patch("calendar_integration.extract_event_times")
def test_auto_schedule_actions(mock_extract, mock_create):
    mock_extract.return_value = ("2025-05-14T12:00:00Z", "2025-05-14T12:30:00Z")
    actions = ["Alice needs to send the report"]

    ci.auto_schedule_actions(actions)

    mock_create.assert_called_once_with(
        title="Alice needs to send the report",
        description="Auto-generated from meeting action item",
        start_time="2025-05-14T12:00:00Z",
        end_time="2025-05-14T12:30:00Z"
    )

def test_extract_people():
    transcript = "Alice and Bob will handle the budget. Charlie will lead."
    people = ci.extract_people(transcript)
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

@patch("calendar_integration.create_calendar_event")
def test_create_calendar_events(mock_create):
    actions = [
        {"text": "Follow up with Alice", "owner": "Alice"},
        {"text": "General meeting review", "owner": "Unassigned"}
    ]
    ci.create_calendar_events(actions)

    assert mock_create.call_count == 2
    titles = [call.args[0] for call in mock_create.call_args_list]
    assert "Follow-up: Alice" in titles
    assert "Meeting Follow-up" in titles

