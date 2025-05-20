"""
json_routes.py

Flask Blueprint routes for JSON-based NLP, feedback, and analytics endpoints
in the AI Meeting Summarizer.

Created by Eric Morse
Date: 2024-05-18

Features:
- /process-json: NLP analysis of meeting transcripts, with event log retrieval.
- /feedback: Accepts and logs user feedback on a meeting.
- Utility to fetch per-meeting event logs for auditability and traceability.

Dependencies: Flask, app.services.nlp_analysis, app.utils.logging_utils, os, json
"""

from flask import Blueprint, request, jsonify
from app.services.nlp_analysis import analyze_transcript
from app.utils.logging_utils import log_event
import os
import json
from datetime import datetime

json_bp = Blueprint('json', __name__)

def log_process_json(data, error=None):
    log_path = os.path.join(os.path.dirname(__file__), "process_json.log")
    with open(log_path, "a", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"\n[{timestamp}] Incoming data: {repr(data)}\n")
        if error:
            f.write(f"[{timestamp}] ERROR: {repr(error)}\n")

            
def get_event_logs_for_meeting(meeting_id):
    """
    Retrieve all event log entries associated with a given meeting ID.

    Args:
        meeting_id (str): Unique meeting identifier.

    Returns:
        list: List of event log dictionaries for the meeting.
    """
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
    """
    Accept and analyze a meeting transcript using NLP.

    Expects:
        Content-Type: application/json
        JSON body:
            {
                "transcript": "...",
                "level": "short"|"detailed" (optional),
                "meeting_id": "unique-id" (optional)
            }

    Returns:
        200: NLP analysis result (with summary, actions, decisions, etc).
        400: JSON error (missing transcript or malformed JSON)
        415: Invalid content type
        500: NLP error
    """
    if not request.is_json:
        return jsonify({"error": "Invalid content type, must be application/json"}), 415
    try:
        data = request.get_json(force=True)
        log_process_json(data)
    except Exception as e:
        log_process_json(getattr(data, 'data', None), error=str(e)) 
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
        log_process_json(getattr(request, 'data', None), error=str(e)) 
        print("Error in /process-json:", e)
        return jsonify({"error": "NLP analysis failed", "details": str(e)}), 500

@json_bp.route('/feedback', methods=['POST'])
def feedback():
    """
    Accepts user feedback about an analysis and logs it.

    Expects:
        Content-Type: application/json
        JSON body:
            {
                "meeting_id": ...,
                "user": ...,
                "score": ...,
                "comments": ...
            }

    Returns:
        200: {"success": True} (feedback logged)
        400: {"success": False, "error": "..."} (bad input)
        415: {"error": "..."} (invalid content type)
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
