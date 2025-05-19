"""
logging_utils.py

Centralized event and transcript logging utilities for the
AI Meeting Summarizer project.

Created by Eric Morse
Date: 2024-05-18

- Structured logging of transcripts and events to timestamped files.
- JSON Lines (.jsonl) for event logs, plaintext for transcripts.
- Convenience wrappers for common event types (actions, decisions, entities, calendar events, errors, feedback, meta, analytics).

Usage:
    from app.utils.logging_utils import log_event, log_transcript_to_file, log_action, ...
"""

import os
import json
from datetime import datetime
from app.utils.logger import logger

def log_transcript_to_file(transcript: str, directory: str = "transcripts") -> str:
    """
    Logs a transcript to a timestamped text file in the specified directory,
    and as a structured transcript event in the event log.

    Args:
        transcript (str): The transcript string.
        directory (str, optional): Target directory (default "transcripts").

    Returns:
        str: Path to the written transcript file, or empty string on failure.
    """
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        os.makedirs(directory, exist_ok=True)
        path = os.path.join(directory, f"transcript_{timestamp}.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(transcript)
        logger.info(f"Transcript logged to {path}")
        # Log also as structured event
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
    Log any structured event as a JSON object in a .jsonl file (one line per event).

    Args:
        event (dict): Event dictionary to log.
        directory (str, optional): Directory for event logs (default "event_logs").

    Returns:
        str: Path to the event log file, or empty string on failure.
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
    """
    Convenience wrapper to log an action event.

    Args:
        action_text (str): Action item description.
        owner (str, optional): Owner of the action.
        meeting_id (str, optional): Meeting identifier.
    """
    log_event({
        "type": "action",
        "text": action_text,
        "owner": owner or "Unassigned",
        "meeting_id": meeting_id
    })

def log_decision(decision_text, meeting_id=None):
    """
    Log a decision event.

    Args:
        decision_text (str): Decision description.
        meeting_id (str, optional): Meeting identifier.
    """
    log_event({
        "type": "decision",
        "text": decision_text,
        "meeting_id": meeting_id
    })

def log_entity_extraction(entities, meeting_id=None):
    """
    Log an entity extraction event.

    Args:
        entities (list): List of entities extracted.
        meeting_id (str, optional): Meeting identifier.
    """
    log_event({
        "type": "entity_extraction",
        "entities": entities,
        "meeting_id": meeting_id
    })

def log_calendar_event(title, start_time, owner=None, status="success", meeting_id=None):
    """
    Log a calendar event creation attempt/result.

    Args:
        title (str): Event title.
        start_time (str): ISO8601 start time.
        owner (str, optional): Event owner.
        status (str, optional): Status ("success", "error", etc.).
        meeting_id (str, optional): Meeting identifier.
    """
    log_event({
        "type": "calendar_event",
        "title": title,
        "start_time": start_time,
        "owner": owner,
        "status": status,
        "meeting_id": meeting_id
    })

def log_error(message, details=None, user=None):
    """
    Log an error event.

    Args:
        message (str): Error message.
        details (any, optional): Additional error details.
        user (str, optional): User identifier.
    """
    log_event({
        "type": "error",
        "message": message,
        "details": details,
        "user": user
    })

def log_feedback(user, score, comments=None):
    """
    Log user feedback on the system.

    Args:
        user (str): User identifier.
        score (int or str): Feedback score or rating.
        comments (str, optional): User comments.
    """
    log_event({
        "type": "feedback",
        "user": user,
        "score": score,
        "comments": comments
    })

def log_meeting_meta(participants, duration, filename=None, meeting_id=None):
    """
    Log meeting metadata (e.g., participant list, duration).

    Args:
        participants (list): List of participant names or IDs.
        duration (float): Duration in seconds/minutes.
        filename (str, optional): Related file name.
        meeting_id (str, optional): Meeting identifier.
    """
    log_event({
        "type": "meeting_meta",
        "participants": participants,
        "duration": duration,
        "filename": filename,
        "meeting_id": meeting_id
    })

def log_analytics_event(event_name, data):
    """
    Log an analytics/custom event.

    Args:
        event_name (str): Name/type of the analytics event.
        data (dict): Custom data payload.
    """
    log_event({
        "type": "analytics",
        "event": event_name,
        "data": data
    })
