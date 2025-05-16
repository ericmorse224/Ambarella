from flask import Blueprint, request, jsonify
from .calendar_integration import create_calendar_event
from datetime import datetime, timedelta

calendar_api = Blueprint('calendar_api', __name__)

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
    # Dummy time window for simplicity
    from datetime import datetime, timedelta
    now = datetime.utcnow()
    start_time = now + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)

    return {
        "title": action_text[:60],
        "description": "Auto-created from meeting action item.",
        "start_time": start_time.isoformat() + "Z",
        "end_time": end_time.isoformat() + "Z",
    }

def create_calendar_event(title, description, start_time, end_time):
    endpoint = "/calendar/v2/calendars/primary/events"
    payload = {
        "event_title": title,
        "location": "",
        "description": description,
        "all_day": False,
        "start_time": start_time,
        "end_time": end_time,
        "timezone": "UTC"
    }

    response = make_authorized_request(endpoint, method="POST", payload=payload)
    if not response.ok:
        raise Exception(f"Zoho calendar event creation failed: {response.text}")

    return response.json()

def get_user_profile():
    endpoint = "/calendar/v2/users/me"
    response = make_authorized_request(endpoint)
    if not response.ok:
        raise Exception(f"Zoho user info failed: {response.text}")
    return response.json()