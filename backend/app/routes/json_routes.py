from flask import Blueprint, request, jsonify
from app.services.nlp_analysis import analyze_transcript
from app.utils.logging_utils import log_event
import os
import json

json_bp = Blueprint('json', __name__)

def get_event_logs_for_meeting(meeting_id):
    directory = "event_logs"
    events = []
    if not meeting_id or not os.path.isdir(directory):
        return events
    for filename in os.listdir(directory):
        if filename.endswith(".jsonl"):
            with open(os.path.join(directory, filename), encoding="utf-8") as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                        if entry.get("meeting_id") == meeting_id:
                            events.append(entry)
                    except Exception:
                        continue
    return events

@json_bp.route('/process-json', methods=['POST'])
def process_json():
    if not request.is_json:
        return jsonify({"error": "Invalid content type, must be application/json"}), 415
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Malformed JSON"}), 400
    transcript = data.get("transcript")
    level = data.get("level", "short")
    meeting_id = data.get("meeting_id")
    if not transcript:
        return jsonify({"error": "Missing transcript"}), 400

    try:
        result = analyze_transcript(transcript, level=level)
        # Attach previous event logs for this meeting, if available
        event_logs = get_event_logs_for_meeting(meeting_id) if meeting_id else []
        result["event_logs"] = event_logs
        result["meeting_id"] = meeting_id
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": "NLP analysis failed", "details": str(e)}), 500

@json_bp.route('/feedback', methods=['POST'])
def feedback():
    """
    Accepts user feedback about an analysis and logs it.
    Expects JSON: {"meeting_id": ..., "user": ..., "score": ..., "comments": ...}
    """
    if not request.is_json:
        return jsonify({"error": "Invalid content type"}), 415
    try:
        data = request.get_json(force=True)
        meeting_id = data.get("meeting_id")
        user = data.get("user", "anonymous")
        score = data.get("score")
        comments = data.get("comments")
        log_event({
            "type": "feedback",
            "meeting_id": meeting_id,
            "user": user,
            "score": score,
            "comments": comments
        })
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
