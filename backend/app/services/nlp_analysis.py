"""
nlp_analysis.py

NLP utilities for extracting summaries, action items, and decisions
from meeting transcripts in the AI Meeting Summarizer project.

Created by Eric Morse
Date: 2024-05-18

Features:
- Group entities by type.
- Extract action items using signal phrases, NLTK tokenization, and POS tagging.
- Extract decisions by phrase matching.
- Summarize by excluding action/decision sentences.
- Full analysis pipeline for meeting transcripts.

Dependencies: nltk, re, app.utils.entity_utils
"""

import re
import nltk
from app.utils.entity_utils import extract_entities, extract_people_from_entities

# Action signal phrases for action extraction
ACTION_PHRASES = [
    "will", "needs to", "need to", "should", "must", "is to", "shall",
    "tasked with", "responsible for", "required to", "assigned to", "supposed to"
]

def group_entities_by_type(entities):
    """
    Group entities by their type (person, organization, location, etc.).

    Args:
        entities (list): List of extracted entity dicts with "entity_type" keys.

    Returns:
        dict: Mapping of {entity_type: [entity_texts, ...]}.
    """
    grouped = {}
    for e in entities:
        etype = e['entity_type'].lower()
        grouped.setdefault(etype, []).append(e['text'])
    return grouped

def extract_actions_nltk(transcript, entities=None):
    """
    Extract action items from a transcript using signal phrases and NLTK POS tagging.

    Args:
        transcript (str): The meeting transcript.
        entities (list or None): List of entity dicts (will be auto-extracted if None).

    Returns:
        tuple: (actions, warnings)
            actions (list): [{ "text": sentence, "owner": str, "confidence": float }]
            warnings (list): Extraction warnings, if any.
    """
    if entities is None:
        entities = extract_entities(transcript)
    people = extract_people_from_entities(entities)
    sentences = nltk.sent_tokenize(transcript)
    actions = []
    warnings = []

    for sentence in sentences:
        tokens = nltk.word_tokenize(sentence)  # Always tokenize first
        tags = nltk.pos_tag(tokens) if tokens else []
        sent_lower = sentence.lower()
        confidence = 0.6
        is_action = False

        # Check for action phrases (strong signal)
        if any(phrase in sent_lower for phrase in ACTION_PHRASES):
            is_action = True
            confidence = 0.95
        else:
            # Check if sentence starts with a verb (imperative, less confident)
            if tags and tags[0][1] == "VB":
                is_action = True
                confidence = 0.85

        if is_action:
            # Try to assign an owner (person mentioned in the sentence)
            owner_candidate = next((p for p in people if p.lower() in sent_lower), None)
            first_word = tokens[0].lower() if tokens else ""
            if (owner_candidate is None or
                owner_candidate.lower() not in [p.lower() for p in people] or
                (tags and tags[0][1] == "VB" and owner_candidate.lower() == first_word)):
                owner = "Someone"
            else:
                owner = owner_candidate

            actions.append({
                "text": sentence.strip(),
                "owner": owner,
                "confidence": confidence
            })

    if not actions:
        warnings.append("No action items detected.")
    return actions, warnings

def extract_decisions(transcript):
    """
    Extract decisions from a meeting transcript by pattern matching.

    Args:
        transcript (str): The full meeting transcript.

    Returns:
        tuple: (decisions, warnings)
            decisions (list): [{ "text": sentence, "confidence": float }]
            warnings (list): Extraction warnings, if any.
    """
    sentences = nltk.sent_tokenize(transcript)
    decisions = []
    warnings = []
    for s in sentences:
        # Pattern matches decision signals
        if re.search(r"\b(decision:|we decided|it was decided|the group decided)\b", s, re.I) or s.lower().startswith("decision:"):
            decisions.append({"text": s.strip(), "confidence": 0.95})
    if not decisions:
        warnings.append("No decisions detected.")
    return decisions, warnings

def extract_summary(transcript, actions=None, decisions=None, level="short"):
    """
    Simple summary extraction by removing action/decision sentences.

    Args:
        transcript (str): Full transcript text.
        actions (list or None): List of action dicts to exclude from summary.
        decisions (list or None): List of decision dicts to exclude from summary.
        level (str): "short" = first 2 non-action/decision sentences,
                     "detailed" = all non-action/decision sentences.

    Returns:
        list: List of summary sentences.
    """
    sentences = nltk.sent_tokenize(transcript)
    action_texts = set(a['text'] for a in (actions or []))
    decision_texts = set(d['text'] for d in (decisions or []))
    base = [s for s in sentences if s not in action_texts and s not in decision_texts]
    if level == "short":
        return base[:2]
    else:
        return base

def analyze_transcript(transcript, level="short"):
    """
    Full meeting transcript analysis pipeline.

    Args:
        transcript (str): Meeting transcript to analyze.
        level (str): Summary level ("short" or "detailed").

    Returns:
        dict: {
            "summary": list of summary sentences,
            "actions": list of extracted actions,
            "decisions": list of extracted decisions,
            "entities": grouped entity dict,
            "warnings": list of warnings,
            "pipeline_version": str (version info)
        }
    """
    warnings = []
    if not transcript or not transcript.strip():
        warnings.append("Transcript is empty or missing.")
        return {
            "summary": [],
            "actions": [],
            "decisions": [],
            "entities": {},
            "warnings": warnings,
            "pipeline_version": "v1.4"
        }

    # Entities extraction and grouping
    entities = extract_entities(transcript)
    grouped_entities = group_entities_by_type(entities)

    # Action extraction (with warnings)
    actions, action_warn = extract_actions_nltk(transcript, entities)
    warnings.extend(action_warn)

    # Decision extraction (with warnings)
    decisions, decision_warn = extract_decisions(transcript)
    warnings.extend(decision_warn)

    # Summary (configurable detail)
    summary = extract_summary(transcript, actions, decisions, level=level)

    return {
        "summary": summary,
        "actions": actions,
        "decisions": decisions,
        "entities": grouped_entities,
        "warnings": warnings,
        "pipeline_version": "v1.4"
    }
