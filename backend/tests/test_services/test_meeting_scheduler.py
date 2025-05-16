from unittest.mock import patch
from app.services.meeting_scheduler import auto_schedule_meetings

@patch("app.services.meeting_scheduler.create_meeting")
def test_create_mock_meeting(mock_create):
    actions = [
        {"owner": "Alice", "text": "Prepare the slides"},
        {"owner": "Bob", "text": "Review the budget"}
    ]
    mock_create.return_value = {"status": "success"}
    result = auto_schedule_meetings(actions)
    assert isinstance(result, list)
    assert len(result) == 2
    mock_create.assert_called()

@patch("app.services.meeting_scheduler.create_meeting")
def test_auto_schedule_with_missing_owner(mock_create):
    actions = [{"owner": "", "text": "Follow up with client", "time": "2025-05-21T15:00:00"}]
    auto_schedule_meetings(actions)
    assert mock_create.called

@patch("app.services.meeting_scheduler.create_meeting", side_effect=Exception("Calendar error"))
def test_auto_schedule_handles_exceptions(mock_create):
    actions = [{"owner": "Bob", "text": "Schedule demo", "time": "2025-05-22T10:00:00"}]
    result = auto_schedule_meetings(actions)
    assert result == []

@patch("app.services.meeting_scheduler.create_meeting")
def test_auto_schedule_empty_list(mock_create):
    result = auto_schedule_meetings([])
    assert result == []

@patch("app.services.meeting_scheduler.create_meeting")
def test_auto_schedule_null_action(mock_create):
    actions = [None]
    result = auto_schedule_meetings(actions)
    assert result == []

@patch("app.services.meeting_scheduler.create_meeting")
def test_auto_schedule_missing_text_field(mock_create):
    actions = [{"owner": "Carol"}]
    mock_create.return_value = {"status": "skipped"}
    result = auto_schedule_meetings(actions)
    assert result[0]["status"] == "skipped"
