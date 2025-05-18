import re
import nltk
from typing import Optional, Tuple, List, Dict, Any

def normalize_name(name: str) -> str:
    """
    Remove common titles from a name and convert to title case.
    Example: "Dr. Bob" -> "Bob"
    """
    name_no_title = re.sub(r'\b(Mr|Ms|Mrs|Dr|Prof|Sir|Madam)\.? ', '', name, flags=re.I)
    return name_no_title.title()

TITLE_PREFIXES = {"Dr.", "Mr.", "Mrs.", "Ms.", "Miss", "Prof.", "Sir", "Madam"}

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

def assign_owner(
    action: str, 
    entities: List[Dict], 
    last_mentioned: Optional[str] = None
) -> Tuple[str, str, bool]:
    """
    Assigns an owner to an action based on extracted person entities.

    Parameters:
    - action: the original action text.
    - entities: list of extracted entities (dictionaries with 'text' and 'entity_type').
    - last_mentioned: optionally, the last mentioned owner to prefer.

    Returns:
    - owner: assigned owner name (string).
    - modified_action: action text (unchanged from input).
    - ambiguous: boolean flag True if multiple owners found (ambiguous).
    """
    # Extract only PERSON entities' text
    people = [e['text'] for e in entities if e.get('entity_type', '').upper() == 'PERSON']

    # Normalize last_mentioned for case-insensitive matching
    last_mentioned_norm = last_mentioned.lower() if last_mentioned else None

    if not people:
        # No owners found, assign generic 'Someone'
        return "Someone", action, True

    if len(people) == 1:
        # Single owner found, return it with original action text
        return people[0], action, False

    # Multiple people found
    # If last_mentioned is in people, assign to that person
    for p in people:
        if last_mentioned_norm and p.lower() == last_mentioned_norm:
            return p, action, False

    # Ambiguous multiple owners, return first owner and mark ambiguous
    return people[0], action, True