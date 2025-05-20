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

# List of key phrases and verbs that signal an action item.
ACTION_PHRASES = [
    # Verbs and signal phrases
    "do", "update", "review", "send", "create", "schedule", "call", "organize",
    "finish", "complete", "start", "plan", "set", "book", "email", "write",
    "check", "fix", "prepare", "assign", "approve", "submit", "remind",
    "arrange", "finalize", "read", "meet", "discuss", "follow", "report",
    "address", "order", "clean", "install", "deploy", "analyze", "collect",
    "help", "join", "follow up", "present", "gather", "share", "investigate",
    "coordinate", "implement", "test", "organize", "begin", "finish",
    "build", "support", "update", "assign", "confirm", "document", "provide",
    "should", "will", "must", "needs to", "has to", "to", "shall"
]

# List of common first names (male, female, unisex) for basic name/entity matching.
EXPECTED_NAMES = [
    # Male names
    "Adam", "Andrew", "Anthony", "Ben", "Brian", "Charles", "Chris",
    "Daniel", "David", "Edward", "Ethan", "Gary", "Jack", "James", "Jason",
    "Jeff", "Joe", "Jonathan", "Joseph", "Josh", "Kevin", "Mark", "Matt",
    "Michael", "Mike", "Nick", "Paul", "Peter", "Richard", "Robert", "Ryan",
    "Sam", "Samuel", "Scott", "Sean", "Steve", "Steven", "Thomas", "Tim",
    "Timothy", "Tom", "Tyler", "Will", "William", "Zach", "Zachary",
    "Fred", "Eric", "John", "Bob", "Carol", "Dave", "Frank", "Aaron", "George", "Greg",
    # Female names
    "Abby", "Amanda", "Amy", "Angela", "Ashley", "Barbara", "Brenda", "Brittany",
    "Caitlin", "Catherine", "Charlotte", "Christina", "Claire", "Courtney",
    "Diana", "Elizabeth", "Emily", "Emma", "Grace", "Hannah", "Heather", "Isabella",
    "Jessica", "Jill", "Julia", "Julie", "Kaitlyn", "Karen", "Katherine", "Katie",
    "Kelly", "Kim", "Kimberly", "Laura", "Lauren", "Lily", "Linda", "Lisa", "Madison",
    "Megan", "Michelle", "Natalie", "Nicole", "Olivia", "Pam", "Patricia", "Rachel",
    "Rebecca", "Samantha", "Sara", "Sarah", "Shannon", "Stephanie", "Susan", "Tara",
    "Taylor", "Victoria", "Wendy", "Alice",  "Erin",  "Susie", "Jane", 
    # Gender-neutral/unisex names
    "Alex", "Casey", "Charlie", "Drew", "Jamie", "Jordan", "Morgan", "Riley", "Robin", "Taylor"
]

def robust_sent_tokenize(text):
    """
    Tokenizes a block of text into sentences, with a fallback to punctuation splitting
    if NLTK's tokenizer yields only one sentence.

    Args:
        text (str): The text to tokenize.

    Returns:
        list of str: List of sentences.
    """
    sentences = nltk.sent_tokenize(text)
    if len(sentences) <= 1:
        sentences = re.split(r'[.,;]\s*', text)
        sentences = [s.strip() for s in sentences if s.strip()]
    return sentences

def find_people_in_sentence(sentence):
    """
    Finds likely person names in a sentence by matching against EXPECTED_NAMES.

    Args:
        sentence (str): The sentence to search.

    Returns:
        list of str: Names found in the sentence.
    """
    tokens = re.findall(r'\b[A-Z][a-z]+\b', sentence)
    people = [t for t in tokens if t in EXPECTED_NAMES]
    return people

def split_actions_within_sentence(sentence, people):
    """
    Splits a sentence with multiple people/entities into separate action items.

    Args:
        sentence (str): The sentence containing potential multiple actions.
        people (list of str): People detected in the sentence.

    Returns:
        list of dict: List of extracted action dicts, each with text and owner.
    """
    actions = []
    if len(people) > 1:
        pattern = r'\b(' + '|'.join(re.escape(name) for name in people) + r')\b'
        splits = re.split(pattern, sentence)
        owner = None
        for part in splits:
            part = part.strip(' ,.;')
            if not part:
                continue
            if part in people:
                owner = part
            elif owner and any(phrase in part for phrase in ACTION_PHRASES):
                actions.append({'text': part, 'owner': owner, 'confidence': 0.95})
        return actions
    return []

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
    # Augment with EXPECTED_NAMES for robust matching
    all_people = list(set(people) | set(EXPECTED_NAMES))
    sentences = robust_sent_tokenize(transcript)

    actions = []
    warnings = []

    for sentence in sentences:
        sent_lower = sentence.lower()
        if any(phrase in sent_lower for phrase in ACTION_PHRASES):
            detected_people = find_people_in_sentence(sentence)
            # Try to split into multiple actions
            multi_actions = split_actions_within_sentence(sentence, detected_people or all_people)
            if multi_actions:
                actions.extend(multi_actions)
                continue
            # Otherwise, assign to first detected person or "Someone"
            owner = detected_people[0] if detected_people else "Someone"
            actions.append({
                "text": sentence.strip(),
                "owner": owner,
                "confidence": 0.95
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
