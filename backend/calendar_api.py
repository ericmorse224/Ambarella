# backend/calendar_api.py
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

        return jsonify({"success": True, "scheduled": results***REMOVED***), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)***REMOVED***), 500
