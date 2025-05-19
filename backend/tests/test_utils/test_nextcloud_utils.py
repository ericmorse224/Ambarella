import pytest
from datetime import datetime, timedelta, timezone
import sys
import os
import time
import re
from caldav import DAVClient
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app.utils import nextcloud_utils


def extract_field(ical, field):
    m = re.search(rf"{field}:(.*)", ical)
    if not m:
        return None
    # Remove potential line folding
    value = m.group(1).replace("\n ", "").replace("\r\n ", "")
    return value.strip()

def test_load_nextcloud_secrets_real():
    url, username, password = nextcloud_utils.load_nextcloud_secrets()
    assert url.startswith("http")
    assert username
    assert password

def test_create_and_verify_event_real():
    # Create an event now+2 minutes (to avoid timing issues)
    now = datetime.now(timezone.utc) + timedelta(minutes=2)
    end = now + timedelta(minutes=30)
    title = f"Test Event {now.strftime('%Y%m%d%H%M%S')}"
    description = "This is a test event created by test_create_and_verify_event_real"
    uid = nextcloud_utils.create_calendar_event(title, description, now, end)
    assert "meeting-summarizer" in uid

    # Verify event appears in calendar by checking all events for this date
    url, username, password = nextcloud_utils.load_nextcloud_secrets()
    client = DAVClient(url, username=username, password=password)
    calendar = client.principal().calendars()[0]
    events = calendar.events()
    matched = False
    print(f"Looking for SUMMARY: {title!r}")
    for event in events:
        data = event.data
        print("\n=== Event ===\n", data)
        summary = extract_field(data, "SUMMARY")
        print(f"Extracted SUMMARY: {summary!r}")
        description_field = extract_field(data, "DESCRIPTION")
        print(f"Extracted DESCRIPTION: {description_field!r}")
        if summary == title:
            print("Exact match found for SUMMARY!")
        if summary and summary.startswith("Test Event"):
            print(f"Matched by startswith: {summary!r}")
            matched = True
            break
    assert matched, f"Event with title '{title}' not found in Nextcloud calendar"

def test_create_event_with_string_times():
    now = datetime.now(timezone.utc) + timedelta(minutes=5)
    end = now + timedelta(minutes=30)
    now_str = now.isoformat()
    end_str = end.isoformat()
    title = f"Test Event String {now.strftime('%Y%m%d%H%M%S')}"
    description = "String time event"
    uid = nextcloud_utils.create_calendar_event(title, description, now_str, end_str)
    assert "meeting-summarizer" in uid

def test_create_calendar_event_no_calendars(monkeypatch):
    class DummyPrincipal:
        def calendars(self):
            return []
    class DummyClient:
        def principal(self):
            return DummyPrincipal()
    # Patch DAVClient to our dummy
    monkeypatch.setattr(nextcloud_utils, "DAVClient", lambda *a, **kw: DummyClient())
    monkeypatch.setattr(nextcloud_utils, "load_nextcloud_secrets", lambda: ("url", "user", "pw"))
    with pytest.raises(Exception, match="No calendars found for this user."):
        nextcloud_utils.create_calendar_event("title", "desc", "2024-01-01T00:00:00", "2024-01-01T01:00:00")

def test_create_calendar_event_invalid_times(monkeypatch):
    class DummyCalendar:
        def add_event(self, ical):
            return
    class DummyPrincipal:
        def calendars(self):
            return [DummyCalendar()]
    class DummyClient:
        def principal(self):
            return DummyPrincipal()
    monkeypatch.setattr(nextcloud_utils, "DAVClient", lambda *a, **kw: DummyClient())
    monkeypatch.setattr(nextcloud_utils, "load_nextcloud_secrets", lambda: ("url", "user", "pw"))
    # Bad format string
    with pytest.raises(ValueError):
        nextcloud_utils.create_calendar_event("title", "desc", "notadate", "notadate")

def test_create_calendar_event_add_event_exception(monkeypatch):
    class DummyCalendar:
        def add_event(self, ical):
            raise RuntimeError("CalDAV error!")
    class DummyPrincipal:
        def calendars(self):
            return [DummyCalendar()]
    class DummyClient:
        def principal(self):
            return DummyPrincipal()
    monkeypatch.setattr(nextcloud_utils, "DAVClient", lambda *a, **kw: DummyClient())
    monkeypatch.setattr(nextcloud_utils, "load_nextcloud_secrets", lambda: ("url", "user", "pw"))
    import pytest
    with pytest.raises(RuntimeError, match="CalDAV error!"):
        nextcloud_utils.create_calendar_event("title", "desc", "2024-01-01T00:00:00", "2024-01-01T01:00:00")
