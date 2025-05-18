# nextcloud_utils.py
import os
import json
from caldav import DAVClient
from datetime import datetime

def load_nextcloud_secrets():
    """
    Loads Nextcloud CalDAV credentials from ~/.app_secrets/env.json
    Returns: (url, username, password)
    """
    secrets_path = os.path.expanduser("~/.app_secrets/env.json")
    with open(secrets_path, "r") as f:
        secrets = json.load(f)
    return (
        secrets["NEXTCLOUD_URL"],
        secrets["NEXTCLOUD_USERNAME"],
        secrets["NEXTCLOUD_PASSWORD"]
    )

from datetime import datetime

def create_calendar_event(title, description, start_time, end_time):
    """
    Creates an event in the user's Nextcloud calendar.
    start_time, end_time are expected to be datetime objects in UTC.
    """
    url, username, password = load_nextcloud_secrets()
    client = DAVClient(url=url, username=username, password=password)
    principal = client.principal()
    calendars = principal.calendars()
    if not calendars:
        raise Exception("No calendars found for this user.")
    calendar = calendars[0]  # Default to first calendar

    # Ensure datetime objects, if strings, parse first (optional)
    if isinstance(start_time, str):
        start_time = datetime.fromisoformat(start_time)
    if isinstance(end_time, str):
        end_time = datetime.fromisoformat(end_time)

    dtstart_str = start_time.strftime('%Y%m%dT%H%M%SZ')
    dtend_str = end_time.strftime('%Y%m%dT%H%M%SZ')

    event_template = f"""BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
UID:{datetime.now().timestamp()}@meeting-summarizer
DTSTART:{dtstart_str}
DTEND:{dtend_str}
SUMMARY:{title}
DESCRIPTION:{description}
END:VEVENT
END:VCALENDAR"""

    calendar.add_event(event_template)

