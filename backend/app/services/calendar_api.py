"""
calendar_api.py

API endpoints for scheduling meetings and creating calendar events
in the AI Meeting Summarizer project.

Created by Eric Morse
Date: 2024-05-18

This module defines routes for event scheduling and integration with
calendar providers. It expects ISO-format times and JSON payloads.

Endpoints:
- POST /api/schedule-actions: Schedule multiple actions as events.
- POST /create-event: Create a single calendar event.

Helper functions:
- create_event_payload
- generate_event_data_from_action

Relies on Flask Blueprint, datetime, and a calendar_integration module.
"""

from flask import Blueprint, request, jsonify
from .calendar_integration import create_calendar_event
from datetime import datetime, timedelta, timezone

calendar_api = Blueprint('calendar_api', __name__)

def create_event_payload(owner, action, start_time, end_time):
    """
    Helper to construct an event payload for calendar integration.

    Args:
        owner (str): Name of meeting owner or responsible person.
        action (str): Description or agenda of the event.
        start_time (str): ISO 8601 start time.
        end_time (str): ISO 8601 end time.

    Returns:
        dict: Dictionary for event creation with title, agenda, attendees, and times.
    """
    owner_str = str(owner).strip() if owner is not None else ""
    action_str = str(action).strip() if action is not None else ""
    start_time_str = str(start_time).strip() if start_time is not None else ""
    end_time_str = str(end_time).strip() if end_time is not None else ""

    title = f"Meeting with {owner_str}" if owner_str else "Meeting with Unassigned"
    attendee_name = owner_str if owner_str else "Unassigned"

    return {
        "title": title,
        "agenda": action_str,
        "start_time": start_time_str,
        "end_time": end_time_str,
        "attendees": [{"name": attendee_name}]
    }

@calendar_api.route('/api/schedule-actions', methods=['POST'])
def schedule_actions():
    """
    Schedule multiple meeting actions as calendar events.

    Expects:
        JSON payload:
            {
                "actions": [
                    {
                        "include": true,
                        "datetime": "YYYY-MM-DDTHH:MM",
                        "text": "Action description",
                        "owner": "Owner name",
                        ...
                    },
                    ...
                ]
            }

    Returns:
        200: { "success": True, "scheduled": [ ... ] }
        500: { "success": False, "error": "description" }
    """
    try:
        actions = request.json.get('actions', [])
        results = []

        for action in actions:
            # Only process actions with an include flag and a datetime
            if not action.get('include') or not action.get('datetime'):
                continue

            title = action.get('text', 'Untitled Action')
            owner = action.get('owner', 'Unassigned')
            start = action['datetime']
            # Schedule as a one-hour event by default
            end = (datetime.fromisoformat(start) + timedelta(hours=1)).isoformat()

            response = create_calendar_event(title, owner, start, end)
            results.append(response)

        return jsonify({"success": True, "scheduled": results}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@calendar_api.route('/create-event', methods=['POST'])
def create_event():
    """
    Create a single calendar event.

    Expects:
        JSON payload:
            {
                "title": "Event Title",
                "description": "Event Description",
                "start_time": "YYYY-MM-DDTHH:MM",
                "end_time": "YYYY-MM-DDTHH:MM"
            }

    Returns:
        200: { "message": "Event created", "event": {...} }
        400: { "error": "Missing required fields" }
        500: { "error": "description" }
    """
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    # Validate required fields
    if not all([title, start_time, end_time]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        event = create_calendar_event(title, description, start_time, end_time)
        return jsonify({'message': 'Event created', 'event': event}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_event_data_from_action(action_text):
    """
    Generate a default event data dictionary for a given action string.

    Args:
        action_text (str): Text of the action or decision.

    Returns:
        dict: Dictionary with title, description, start_time, and end_time
              (scheduled for 1 hour, starting 1 day from now).
    """
    now = datetime.now(timezone.utc)
    start_time = now + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)
    start = start_time.strftime('%Y-%m-%dT%H:%M')
    end = end_time.strftime('%Y-%m-%dT%H:%M')
    return {
        "title": action_text[:60],
        "description": "Auto-created from meeting action item.",
        "start_time": start,
        "end_time": end,
    }
