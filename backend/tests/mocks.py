from unittest.mock import MagicMock

def mock_transcribe_success():
    return "This is a mocked transcript."

def mock_summary_and_extraction():
    return """Summary:
- This is a summary

Action Items:
- Alice needs to send the email

Decisions:
- Proceed with launch
"""

def mock_calendar_event_success(title, description, start_time, end_time):
    return {"status": "success", "event": {"title": title}}

def mock_meeting_creation(title, agenda, start_time):
    return {"status": "success", "meeting_url": "https://mock.zoho.meeting"}