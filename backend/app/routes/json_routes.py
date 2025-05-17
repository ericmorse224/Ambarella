from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from nltk.tokenize import sent_tokenize
from app.services.llm_utils import generate_summary_and_extraction, parse_llm_sections
from app.utils.entity_utils import extract_people, assign_actions_to_people, assign_owner
from app.utils.zoho_utils import create_calendar_event
from app.utils.logger import logger
from app.services.nlp_analysis import analyze_transcript  # you should move this if it exists
from werkzeug.exceptions import BadRequest, UnsupportedMediaType

json_bp = Blueprint('json', __name__)

@json_bp.route("/process-json", methods=["POST"])
def process_json():
    try:
        if not request.is_json:
            return jsonify({"error": "Invalid content type. Must be application/json."}), 415

        try:
            data = request.get_json(force=True)
        except Exception as json_err:
            return jsonify({"error": f"Malformed JSON: {str(json_err)}"}), 400

        if not data or "transcript" not in data:
            return jsonify({"error": "Missing transcript"}), 400

        transcript = data["transcript"]
        result = analyze_transcript(transcript)
        return jsonify(result)

    except Exception as e:
        logger.error("Error in /process-json", exc_info=True)
        return jsonify({"error": str(e)}), 500

