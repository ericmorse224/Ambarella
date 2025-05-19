"""
calendar_integration.py

Backend utilities for integrating meeting actions and decisions
with the calendar system (Nextcloud) for the AI Meeting Summarizer.

Created by Eric Morse
Date: 2024-05-18

Features:
- Parse dates/times from action items using dateparser.
- Create calendar events for assigned actions/owners.
- Log all event creation attempts (success and failure).
"""

from datetime import datetime, timedelta, timezone
from app.utils.logger import logger
from app.utils.logging_utils import log_event
import re
from app.utils.nextcloud_utils import create_calendar_event
import dateparser
from app.utils.entity_utils import extract_people_from_entities, assign_actions_to_people

def extract_event_times(action_text):
    """
    Parse a date/time from an action item using dateparser.

    Args:
        action_text (str): Action description (may contain date/time phrases).

    Returns:
        tuple: (start_time_iso, end_time_iso), both as ISO8601 UTC strings.
               Defaults to 1 hour from now, 30 minutes duration if not found.
    """
    parsed_time = dateparser.parse(action_text, settings={"PREFER_DATES_FROM": "future"})
    if not parsed_time:
        # Default: 1 hour from now
        parsed_time = datetime.now(timezone.utc) + timedelta(hours=1)
    end_time = parsed_time + timedelta(minutes=30)
    return parsed_time.isoformat() + "Z", end_time.isoformat() + "Z"

# Uncomment and adapt this function if you want fully automatic scheduling.
# def auto_schedule_actions(actions):
#     """
#     Automatically schedule all provided actions as events in Nextcloud.
#     Each action is a string. Start/end are auto-parsed or defaulted.
#     On error, logs to logger and as an event.
#     """
#     for action in actions:
#         logger.info(f"Scheduling: {action}")
#         start_time, end_time = extract_event_times(action)
#         try:
#             response = create_calendar_event(
#                 title=action,
#                 description="Auto-generated from meeting action item",
#                 start_time=start_time,
#                 end_time=end_time
#             )
#             logger.info(f"Calendar response: {response}")
#             log_event({
#                 "type": "calendar_event",
#                 "title": action,
#                 "start_time": start_time,
#                 "end_time": end_time,
#                 "status": "success",
#                 "response": str(response)
#             })
#         except Exception as e:
#             logger.error(f"Calendar event creation failed: {e}")
#             log_event({
#                 "type": "calendar_event",
#                 "title": action,
#                 "start_time": start_time,
#                 "end_time": end_time,
#                 "status": "error",
#                 "error": str(e)
#             })

def create_calendar_events(assigned_actions):
    """
    Create calendar events for a list of assigned actions.

    Each action should be a dictionary with at least:
      - "text": The action description
      - "owner": The assigned owner or "Unassigned"

    Logs both success and failure events.

    Args:
        assigned_actions (list): List of {"text": str, "owner": str} dictionaries.

    Side Effects:
        - Calls Nextcloud via create_calendar_event()
        - Logs event creation results via log_event().
    """
    for item in assigned_actions:
        title = f"Follow-up: {item['owner']}" if item['owner'] != "Unassigned" else "Meeting Follow-up"
        print(f"BACKEND: Attempting to create event '{title}'")
        description = item['text'] + f"\n\nOwner: {item['owner']}"
        # Default to event starting 1 hour from now, 30 min duration
        start_time = datetime.now(timezone.utc) + timedelta(hours=1)
        end_time = start_time + timedelta(minutes=30)
        try:
            response = create_calendar_event(
                title, description, start_time.isoformat(), end_time.isoformat()
            )
            log_event({
                "type": "calendar_event",
                "title": title,
                "description": description,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "owner": item['owner'],
                "status": "success",
                "response": str(response)
            })
        except Exception as e:
            logger.error(f"Calendar event creation failed: {e}")
            log_event({
                "type": "calendar_event",
                "title": title,
                "description": description,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "owner": item['owner'],
                "status": "error",
                "error": str(e)
            })
