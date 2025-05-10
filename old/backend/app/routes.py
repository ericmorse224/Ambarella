### backend/app/routes.py
from flask import Blueprint, request, jsonify
from .utils import load_meeting_json
from .summarization import summarize_transcript
from .extraction import extract_actions, extract_decisions

main = Blueprint('main', __name__)

@main.route("/process-json", methods=["POST"])
def process_json():
    data = request.get_json()
    transcript = data.get("transcript", [])

    summary = summarize_transcript(transcript)
    actions = extract_actions(transcript)
    decisions = extract_decisions(transcript)

    return jsonify({
        "summary": summary,
        "actions": actions,
        "decisions": decisions
    ***REMOVED***)
