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


#@json_bp.route('/process-json', methods=['POST'])
#def process_json():
#    try:
#        data = request.get_json()
#        transcript = data.get("transcript", "")
#        entities = data.get("entities", [])
#
#        if not transcript:
#            return jsonify({"error": "Transcript missing."}), 400
#
#        from app.services.nlp_analysis import analyze_transcript
#        from app.utils.entity_utils import extract_people_from_entities
#        from app.utils.zoho_utils import create_calendar_event
#
#        # Use detected entity names as fallback
#        people = extract_people_from_entities(entities)
#
#        result = analyze_transcript(transcript)
#        
#        for action in result.get("actions", []):
#            try:
#                # Fill missing owner using fallback people list
#                if action["owner"] == "Someone" and people:
#                    for p in people:
#                        if p.lower() in action["text"].lower():
#                            action["owner"] = p
#                            break
#
#                create_calendar_event(
#                    title=f"Follow-up: {action['owner']}",
#                    description=action['text'],
#                    start_time=action['start'],
#                    end_time=action['end']
#                )
#            except Exception as e:
#                logger.warning(f"Calendar event error for action '{action['text']}': {e}")
#
#        return jsonify(result)
#
#    except Exception as e:
#        logger.exception("Error in /process-json")
#        return jsonify({"error": str(e)}), 500

@json_bp.route('/process-json-for-AB-testing', methods=['POST'])
def process_json_for_ab_testing():
    try:
        data = request.get_json()
        transcript = data.get("transcript", "")
        entities = data.get("entities", [])

        if not transcript:
            return jsonify({"error": "Transcript missing."}), 400

        from nltk.tokenize import sent_tokenize
        from app.utils.entity_utils import extract_people, assign_actions_to_people, extract_people_from_entities
        from app.utils.zoho_utils import create_calendar_event

        sentences = sent_tokenize(transcript)
        summary, actions, decisions = [], [], []
        action_keywords = ["will", "must", "should", "needs to", "is responsible for"]

        for sentence in sentences:
            lower = sentence.lower()
            if any(k in lower for k in action_keywords):
                actions.append(sentence)
            elif "decision" in lower or "decided" in lower:
                decisions.append(sentence)
            else:
                summary.append(sentence)

        people = extract_people_from_entities(entities) or extract_people(transcript)
        assigned_actions = assign_actions_to_people(actions, people)

        for item in assigned_actions:
            title = f"Follow-up: {item['owner']}" if item['owner'] != "Unassigned" else "Meeting Follow-up"
            description = item['text'] + f"\n\nOwner: {item['owner']}"
            start_time = datetime.now() + timedelta(hours=1)
            end_time = start_time + timedelta(minutes=30)

            try:
                create_calendar_event(title, description, start_time.isoformat(), end_time.isoformat())
            except Exception as e:
                logger.warning(f"AB test calendar event error: {e}")

        return jsonify({
            "summary": summary,
            "actions": [a['text'] for a in assigned_actions],
            "decisions": decisions
        })

    except Exception as e:
        logger.exception("Error in /process-json-for-AB-testing")
        return jsonify({"error": str(e)}), 500
