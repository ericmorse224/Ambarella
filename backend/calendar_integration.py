from datetime import datetime, timedelta, UTC
import logging
import re
from zoho_utils import create_calendar_event

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
