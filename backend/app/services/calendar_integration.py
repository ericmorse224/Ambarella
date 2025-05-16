from datetime import datetime, timedelta, UTC
from app.utils.logger import logger
import re
from app.utils.zoho_utils import create_calendar_event
import dateparser
from app.utils.entity_utils import extract_people, assign_actions_to_people

def extract_event_times(action_text):
    """Parses a date/time string from the action item."""
    parsed_time = dateparser.parse(action_text, settings={"PREFER_DATES_FROM": "future"})
    if not parsed_time:
        parsed_time = datetime.now(UTC) + timedelta(hours=1)
    end_time = parsed_time + timedelta(minutes=30)
    return parsed_time.isoformat() + "Z", end_time.isoformat() + "Z"

def auto_schedule_actions(actions):
    for action in actions:
        logger.info(f"Scheduling: {action}")
        start_time, end_time = extract_event_times(action)
        response = create_calendar_event(
            title=action,
            description="Auto-generated from meeting action item",
            start_time=start_time,
            end_time=end_time
        )
        logger.info(f"Zoho response: {response}")

def create_calendar_events(assigned_actions):
    for item in assigned_actions:
        title = f"Follow-up: {item['owner']}" if item['owner'] != "Unassigned" else "Meeting Follow-up"
        description = item['text'] + f"\n\nOwner: {item['owner']}"
        start_time = datetime.now(UTC) + timedelta(hours=1)
        end_time = start_time + timedelta(minutes=30)

        try:
            create_calendar_event(title, description, start_time.isoformat(), end_time.isoformat())
        except Exception as e:
            logger.error(f"Calendar event creation failed: {e}")

