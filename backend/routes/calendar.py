from flask import Blueprint, request, jsonify
from zoho_utils import create_calendar_event

calendar_bp = Blueprint('calendar', __name__)

@calendar_bp.route('/create-event', methods=['POST'])
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

