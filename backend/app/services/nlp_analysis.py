from datetime import datetime, timedelta
from app.services.llm_utils import generate_summary_and_extraction, parse_llm_sections
from app.utils.entity_utils import assign_owner, extract_people
from app.utils.logger import logger

def analyze_transcript(transcript):
    """
    Analyze transcript using LLM to extract summary, action items, decisions.
    Assign owners to actions.
    """
    raw_output = generate_summary_and_extraction(transcript)

    # Ensure raw_output is a string to avoid regex errors
    if isinstance(raw_output, dict):
        logger.warning("LLM returned a dict instead of string; converting to string.")
        raw_output = str(raw_output)

    parsed = parse_llm_sections(raw_output) or {}

    assigned_actions = []
    ambiguous_actions = []
    last_mentioned = None

    people = extract_people(transcript)

    for action_obj in parsed.get("actions", []):
        if not isinstance(action_obj, dict) or "text" not in action_obj:
            logger.warning(f"Skipping malformed action: {action_obj}")
            continue

        action_text = action_obj["text"]
        owner, assignment, is_ambiguous = assign_owner(action_text, people, last_mentioned)

        if owner != "Someone":
            last_mentioned = owner

        start_time = datetime.now() + timedelta(hours=1)
        end_time = start_time + timedelta(minutes=30)

        enriched_action = {
            "text": assignment,
            "owner": owner,
            "is_ambiguous": is_ambiguous,
            "start": start_time.isoformat(),
            "end": end_time.isoformat()
        }

        if is_ambiguous:
            ambiguous_actions.append(enriched_action)
        else:
            assigned_actions.append(enriched_action)

    return {
        "summary": parsed.get("summary", ""),
        "actions": assigned_actions + ambiguous_actions,
        "decisions": parsed.get("decisions", []),
        "raw_output": raw_output
    }
