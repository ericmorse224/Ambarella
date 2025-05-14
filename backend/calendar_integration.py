from datetime import datetime, timedelta, UTC
import logging
import re
from zoho_utils import create_calendar_event
import dateparser

logging.basicConfig(level=logging.INFO)

def extract_event_times(action_text):
    """Parses a date/time string from the action item."""
    parsed_time = dateparser.parse(action_text, settings={"PREFER_DATES_FROM": "future"***REMOVED***)
    if not parsed_time:
        parsed_time = datetime.now(UTC) + timedelta(hours=1)
    end_time = parsed_time + timedelta(minutes=30)
    return parsed_time.isoformat() + "Z", end_time.isoformat() + "Z"

def auto_schedule_actions(actions):
    for action in actions:
        logging.info(f"Scheduling: {action***REMOVED***")
        start_time, end_time = extract_event_times(action)
        response = create_calendar_event(
            title=action,
            description="Auto-generated from meeting action item",
            start_time=start_time,
            end_time=end_time
        )
        logging.info(f"Zoho response: {response***REMOVED***")

def extract_people(transcript):
    """
    Extract capitalized words that appear to be names.
    Ignores common non-name words by using a basic exclusion list.
    """
    common_words = {"The", "This", "That", "He", "She", "It", "They", "We", "You", "I",
                    "Needs", "Should", "Will", "Must", "Decision", "Meeting", "Follow", "Up"***REMOVED***
    words = re.findall(r'\b[A-Z][a-z]{2,***REMOVED***\b', transcript)
    people = [word for word in set(words) if word not in common_words]
    return people

def assign_actions_to_people(actions, people):
    assigned = []
    for action in actions:
        owner = next((p for p in people if p.lower() in action.lower()), "Unassigned")
        assigned.append({"text": action, "owner": owner***REMOVED***)
    return assigned

def create_calendar_events(assigned_actions):
    for item in assigned_actions:
        title = f"Follow-up: {item['owner']***REMOVED***" if item['owner'] != "Unassigned" else "Meeting Follow-up"
        description = item['text'] + f"\n\nOwner: {item['owner']***REMOVED***"
        start_time = datetime.now(UTC) + timedelta(hours=1)
        end_time = start_time + timedelta(minutes=30)

        try:
            create_calendar_event(title, description, start_time.isoformat(), end_time.isoformat())
        except Exception as e:
            logging.error(f"Calendar event creation failed: {e***REMOVED***")
