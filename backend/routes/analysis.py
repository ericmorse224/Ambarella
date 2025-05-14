from flask import Blueprint, request, jsonify
from utils.nlp import analyze_transcript
from utils.zoho_event import create_calendar_event

analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/process-json', methods=['POST'])
def process_json():
    data = request.get_json()
    transcript = data.get("transcript", "")
    if not transcript:
        return jsonify({"error": "No transcript provided"***REMOVED***), 400

    try:
        result = analyze_transcript(transcript)

        # Auto-create calendar events for each action item
        for action in result.get("actions", []):
            create_calendar_event(action)

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)***REMOVED***), 500
