"""
nextcloud_utils.py

Nextcloud CalDAV integration utilities for the AI Meeting Summarizer.

Created by Eric Morse
Date: 2024-05-18

Features:
- Loads Nextcloud credentials from a local secret file.
- Creates calendar events in the user's Nextcloud calendar via CalDAV.
- Designed for secure, programmatic event management.

Dependencies:
    - caldav
    - Python standard library (os, json, datetime)
    - Secret file: ~/.app_secrets/env.json
"""

import os
import json
from caldav import DAVClient
from datetime import datetime

def load_nextcloud_secrets():
    """
    Load Nextcloud CalDAV credentials from ~/.app_secrets/env.json.

    Returns:
        tuple: (url, username, password)

    Raises:
        FileNotFoundError: If the secrets file does not exist.
        KeyError: If any of the required fields are missing in the secrets file.
    """
    secrets_path = os.path.expanduser("~/.app_secrets/env.json")
    with open(secrets_path, "r") as f:
        secrets = json.load(f)
    return (
        secrets["NEXTCLOUD_URL"],
        secrets["NEXTCLOUD_USERNAME"],
        secrets["NEXTCLOUD_PASSWORD"]
    )

def create_calendar_event(title, description, start_time, end_time):
    """
    Create an event in the user's Nextcloud calendar.

    Args:
        title (str): Event title.
        description (str): Event description/notes.
        start_time (datetime|str): Event start (UTC datetime or ISO 8601 string).
        end_time (datetime|str): Event end (UTC datetime or ISO 8601 string).

    Returns:
        str: Event UID (unique identifier).

    Raises:
        Exception: If calendar is not found or event creation fails.
    """
    url, username, password = load_nextcloud_secrets()
    client = DAVClient(url=url, username=username, password=password)
    principal = client.principal()
    calendars = principal.calendars()
    if not calendars:
        raise Exception("No calendars found for this user.")
    calendar = calendars[0]  # Default to first available calendar

    # Ensure start_time and end_time are datetime objects
    if isinstance(start_time, str):
        start_time = datetime.fromisoformat(start_time)
    if isinstance(end_time, str):
        end_time = datetime.fromisoformat(end_time)

    dtstart_str = start_time.strftime('%Y%m%dT%H%M%SZ')
    dtend_str = end_time.strftime('%Y%m%dT%H%M%SZ')
    uid = f"{datetime.now().timestamp()}@meeting-summarizer"

    event_template = f"""BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
UID:{uid}
DTSTART:{dtstart_str}
DTEND:{dtend_str}
SUMMARY:{title}
DESCRIPTION:{description}
END:VEVENT
END:VCALENDAR"""

    try:
        calendar.add_event(event_template)
        print(f"Event created: {title}, UID: {uid}, {dtstart_str}–{dtend_str}")
        return uid
    except Exception as e:
        print(f"Failed to create event: {e}")
        raise
