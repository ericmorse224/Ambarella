import re
import nltk
from typing import List, Dict, Tuple, Any

TITLE_PREFIXES = {"Dr.", "Mr.", "Mrs.", "Ms.", "Miss", "Prof.", "Sir", "Madam"}

def normalize_name(name: str) -> str:
    """
    Remove common titles from a name and convert to title case.
    Example: "Dr. Bob" -> "Bob"
    """
    name_no_title = re.sub(r'\b(Mr|Ms|Mrs|Dr|Prof|Sir|Madam)\.? ', '', name, flags=re.I)
    return name_no_title.title()

def extract_entities(text: str) -> List[dict]:
    """
    Extract named person entities from text using NLTK, including common title prefixes.
    """
    tokens = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(tokens)
    chunked = nltk.ne_chunk(pos_tags, binary=False)

    entities = []
    i = 0
    while i < len(chunked):
        subtree = chunked[i]
        if hasattr(subtree, 'label') and subtree.label() == 'PERSON':
            person_tokens = [token for token, pos in subtree.leaves()]
            # Look backwards for titles
            j = i - 1
            while j >= 0:
                prev = chunked[j]
                if not hasattr(prev, 'label') and prev[0] in TITLE_PREFIXES:
                    person_tokens.insert(0, prev[0])
                    j -= 1
                else:
                    break
            entity_text = " ".join(person_tokens)
            entities.append({"text": entity_text, "entity_type": "PERSON"})
            i += 1
        else:
            i += 1

    # Also add standalone titles followed by names if missed
    # (Optional: This can be added if needed by scanning tokens)

    return entities

def clean_name(name: str) -> str:
    for title in TITLE_PREFIXES:
        if name.startswith(title):
            return name[len(title):].strip()
    return name

def extract_people_from_entities(entities: List[Dict[str, Any]]) -> List[str]:
    """
    Extract unique person names from entity list.

    Args:
        entities (List[Dict]): Entities from extract_entities.

    Returns:
        List[str]: Unique list of person names.
    """
    return list(set(clean_name(e['text']) for e in entities if isinstance(e,dict) and e.get('entity_type', '').upper() == 'PERSON'))

def extract_probable_people(text: str) -> List[str]:
    """
    Fallback extraction of probable person names by capturing capitalized words 
    and filtering out common non-name words.

    Args:
        text (str): The input text.

    Returns:
        List[str]: List of probable person names.
    """
    common_words = {
        "The", "This", "That", "He", "She", "It", "They", "We", "You", "I",
        "Needs", "Should", "Will", "Must", "Decision", "Meeting", "Follow", "Up"
    }
    candidates = re.findall(r'\b[A-Z][a-z]{2,}\b', text)
    people = [word for word in set(candidates) if word not in common_words]
    return people

def assign_actions_to_people(actions: List[str], people: List[str]) -> List[Dict[str, str]]:
    """
    Assign each action to the first matching person found in the action text.
    If no person matches, assign 'Unassigned'.

    Args:
        actions (List[str]): List of action descriptions.
        people (List[str]): List of person names.

    Returns:
        List[Dict]: List with keys:
            - 'text': action text
            - 'owner': assigned person or 'Unassigned'
    """
    assigned = []
    for action in actions:
        owner = next((p for p in people if p.lower() in action.lower()), "Unassigned")
        assigned.append({"text": action, "owner": owner})
    return assigned

def assign_owner(action: str, entities: List[Dict[str, Any]], last_mentioned: str = None) -> Tuple[str, str, bool]:
    """
    Assign an owner to an action by matching PERSON entities or falling back on pronouns.
    Preserves full original entity text (including titles/honorifics).

    Args:
        action: Action description text.
        entities: List of named entities detected in context.
        last_mentioned: Optional last mentioned person for pronoun resolution.

    Returns:
        Tuple of:
          - owner (str): Full original name with titles.
          - assigned_action (str): Reformatted action string with owner.
          - is_ambiguous (bool): True if owner assignment is uncertain.
    """

    TITLE_PREFIXES = {"Dr.", "Mr.", "Mrs.", "Ms.", "Miss", "Prof.", "Sir", "Madam"}

    def normalize_name(name: str) -> str:
        # Lowercase and strip titles for matching keys
        return re.sub(r'\b(Mr|Ms|Mrs|Dr|Prof|Sir|Madam)\.? ', '', name, flags=re.I).lower()

    normalized_to_original = {
        normalize_name(e['text']): e['text']
        for e in entities if e.get('entity_type', '').upper() == 'PERSON'
    }
    person_entities = list(normalized_to_original.keys())

    pronoun_map = {
        "he": last_mentioned,
        "she": last_mentioned,
        "they": last_mentioned,
        "his": last_mentioned,
        "her": last_mentioned,
        "them": last_mentioned
    }

    lower_action = action.lower()
    is_ambiguous = False

    # Tokenize action for matching
    action_tokens = re.findall(r'\b\w+\b', lower_action)

    for person_norm in person_entities:
        person_tokens = person_norm.split()
        # Check if person tokens appear as sequence in action tokens
        pattern = r'\b' + r'\s+'.join(map(re.escape, person_tokens)) + r'\b'
        if re.search(pattern, lower_action):
            # Remove the owner tokens from action text (case-insensitive)
            cleaned_action = re.sub(pattern, '', action, flags=re.I).strip()
            cleaned_action = re.sub(r'\s{2,}', ' ', cleaned_action)

            # Remove any leftover titles from cleaned_action, but preserve owner as-is
            cleaned_action = re.sub(
                r'\b(?:' + '|'.join([re.escape(t) for t in TITLE_PREFIXES]) + r')\.?\s',
                '',
                cleaned_action,
                flags=re.I
            ).strip()

            owner = normalized_to_original[person_norm]

            # Determine if "needs to" should be added or not
            # Add "needs to" only if cleaned_action does not start with a verb phrase already
            if cleaned_action and not re.match(r'^(needs to|will|should|must|shall|can|could|would|may|might|have to|has to|need to|do|does|did)\b', cleaned_action, re.I):
                assigned_action = f"{owner} needs to {cleaned_action}".strip()
            else:
                assigned_action = f"{owner} {cleaned_action}".strip()

            return owner, assigned_action, is_ambiguous

    # Pronoun fallback preserving casing of last_mentioned
    for pronoun, fallback in pronoun_map.items():
        if pronoun in lower_action and fallback:
            assigned_action = f"{fallback} needs to {action}".strip()
            return fallback, assigned_action, is_ambiguous

    # Default ambiguous fallback
    assigned_action = f"Someone needs to {action}".strip()
    is_ambiguous = True
    return "Someone", assigned_action, is_ambiguous
