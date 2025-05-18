import os
import json
from datetime import datetime
from app.utils.logger import logger

def log_transcript_to_file(transcript: str, directory: str = "transcripts") -> str:
    """
    Logs the transcript to a timestamped file in the specified directory.
    Returns the file path.
    """
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        os.makedirs(directory, exist_ok=True)
        path = os.path.join(directory, f"transcript_{timestamp}.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(transcript)
        logger.info(f"Transcript logged to {path}")
        # Also log as a structured event
        log_event({
            "type": "transcript",
            "timestamp": timestamp,
            "transcript": transcript
        })
        return path
    except Exception as e:
        logger.error(f"Failed to log transcript: {e}")
        return ""

def log_event(event: dict, directory: str = "event_logs") -> str:
    """
    Logs any structured event (action, decision, entity extraction, calendar event, error, etc.)
    as a JSON object in a .jsonl file (one line per event).
    Returns the file path.
    """
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        os.makedirs(directory, exist_ok=True)
        path = os.path.join(directory, f"event_log_{today}.jsonl")
        # Always add a timestamp and event type if missing
        event_record = {
            "logged_at": datetime.now().isoformat(),
            **event
        }
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event_record) + "\n")
        logger.info(f"Event logged to {path}: {event_record}")
        return path
    except Exception as e:
        logger.error(f"Failed to log event: {e}")
        return ""

# --- Example wrappers for different types (optional, for convenience) ---

def log_action(action_text, owner=None, meeting_id=None):
    log_event({
        "type": "action",
        "text": action_text,
        "owner": owner or "Unassigned",
        "meeting_id": meeting_id
    })

def log_decision(decision_text, meeting_id=None):
    log_event({
        "type": "decision",
        "text": decision_text,
        "meeting_id": meeting_id
    })

def log_entity_extraction(entities, meeting_id=None):
    log_event({
        "type": "entity_extraction",
        "entities": entities,
        "meeting_id": meeting_id
    })

def log_calendar_event(title, start_time, owner=None, status="success", meeting_id=None):
    log_event({
        "type": "calendar_event",
        "title": title,
        "start_time": start_time,
        "owner": owner,
        "status": status,
        "meeting_id": meeting_id
    })

def log_error(message, details=None, user=None):
    log_event({
        "type": "error",
        "message": message,
        "details": details,
        "user": user
    })

def log_feedback(user, score, comments=None):
    log_event({
        "type": "feedback",
        "user": user,
        "score": score,
        "comments": comments
    })

def log_meeting_meta(participants, duration, filename=None, meeting_id=None):
    log_event({
        "type": "meeting_meta",
        "participants": participants,
        "duration": duration,
        "filename": filename,
        "meeting_id": meeting_id
    })

def log_analytics_event(event_name, data):
    log_event({
        "type": "analytics",
        "event": event_name,
        "data": data
    })
