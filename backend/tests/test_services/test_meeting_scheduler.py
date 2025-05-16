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
