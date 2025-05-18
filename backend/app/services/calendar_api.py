from flask import Blueprint, request, jsonify
from .calendar_integration import create_calendar_event
from datetime import datetime, timedelta, timezone  # added timezone import

calendar_api = Blueprint('calendar_api', __name__)

def create_event_payload(owner, action, start_time, end_time):
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
    try:
        actions = request.json.get('actions', [])
        results = []

        for action in actions:
            if not action.get('include') or not action.get('datetime'):
                continue

            title = action.get('text', 'Untitled Action')
            owner = action.get('owner', 'Unassigned')
            start = action['datetime']
            # Simple default: schedule for 1 hour
            end = (datetime.fromisoformat(start) + timedelta(hours=1)).isoformat()

            response = create_calendar_event(title, owner, start, end)
            results.append(response)

        return jsonify({"success": True, "scheduled": results}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@calendar_api.route('/create-event', methods=['POST'])
def create_event():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    if not all([title, start_time, end_time]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        event = create_calendar_event(title, description, start_time, end_time)
        return jsonify({'message': 'Event created', 'event': event}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_event_data_from_action(action_text):
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
