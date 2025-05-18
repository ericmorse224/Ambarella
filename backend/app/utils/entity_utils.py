import re
import nltk
from typing import Optional, Tuple, List, Dict, Any

TITLE_PREFIXES = {"Dr.", "Mr.", "Mrs.", "Ms.", "Miss", "Prof.", "Sir", "Madam"}

def normalize_name(name: str) -> str:
    """
    Remove common titles from a name and convert to title case.
    Example: "Dr. Bob" -> "Bob"
    """
    name_no_title = re.sub(r'\b(Mr|Ms|Mrs|Dr|Prof|Sir|Madam)\.? ', '', name, flags=re.I)
    return name_no_title.title()

def clean_name(name: str) -> str:
    """
    Strip known titles from the start of a name, preserve rest as-is.
    """
    for title in TITLE_PREFIXES:
        if name.startswith(title):
            return name[len(title):].strip()
    return name

def extract_entities(text: str) -> List[Dict[str, Any]]:
    """
    Extract named person entities from text using NLTK, including common title prefixes.
    Returns list of entities with text and entity_type 'PERSON'.
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
            # Look backwards for titles (case insensitive)
            j = i - 1
            while j >= 0:
                prev = chunked[j]
                if not hasattr(prev, 'label') and prev[0].lower().rstrip('.') in {t.lower().rstrip('.') for t in TITLE_PREFIXES}:
                    person_tokens.insert(0, prev[0])
                    j -= 1
                else:
                    break
            entity_text = " ".join(person_tokens)
            # Prevent adding only a title as an entity
            # Only add if there is at least one non-title token
            non_title_tokens = [t for t in person_tokens if t.lower().rstrip('.') not in {x.lower().rstrip('.') for x in TITLE_PREFIXES}]
            if len(non_title_tokens) > 0:
                entities.append({"text": entity_text, "entity_type": "PERSON"})
            i += 1
        else:
            i += 1

    # Supplement with probable people if none or some names missing
    probable_people = extract_probable_people(text)
    # Add probable people as PERSON if not already in entities
    existing_names = set(e['text'].lower() for e in entities)
    for p in probable_people:
        if p.lower() not in existing_names:
            entities.append({"text": p, "entity_type": "PERSON"})

    return entities

def extract_people_from_entities(entities: List[Dict[str, Any]]) -> List[str]:
    """
    Extract unique person names from entity list, clean titles and normalize casing.

    Args:
        entities: List of entity dicts from extract_entities.

    Returns:
        List of unique cleaned and normalized person names.
    """
    cleaned_people = set()
    for e in entities:
        if isinstance(e, dict) and e.get('entity_type', '').upper() == 'PERSON':
            name = clean_name(e['text'])
            normalized = normalize_name(name)
            cleaned_people.add(normalized)
    return list(cleaned_people)

def extract_probable_people(text: str) -> List[str]:
    """
    Fallback extraction of probable person names by capturing capitalized words 
    and filtering out common non-name words.

    Args:
        text: input string

    Returns:
        List of probable person names.
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
        actions: list of action strings
        people: list of normalized person names

    Returns:
        List of dicts with keys 'text' and 'owner'
    """
    assigned = []
    for action in actions:
        owner = next((p for p in people if p.lower() in action.lower()), "Unassigned")
        assigned.append({"text": action, "owner": owner})
    return assigned

def assign_owner(
    action: str, 
    entities: List[Dict[str, Any]], 
    last_mentioned: Optional[str] = None
) -> Tuple[str, str, bool]:
    """
    Assigns an owner to an action based on extracted person entities.

    Parameters:
    - action: the original action text.
    - entities: list of extracted entities (dicts with 'text' and 'entity_type').
    - last_mentioned: optional last mentioned owner to prefer.

    Returns:
    - owner: assigned owner name (string, normalized with title stripped).
    - modified_action: action text (unchanged).
    - ambiguous: True if multiple owners found, else False.
    """
    # Extract and normalize PERSON entities
    people = []
    for e in entities:
        if e.get('entity_type', '').upper() == 'PERSON':
            name = clean_name(e['text'])
            normalized = normalize_name(name)
            people.append(normalized)

    last_mentioned_norm = normalize_name(last_mentioned) if last_mentioned else None

    if not people:
        return "Someone", action, True

    if len(people) == 1:
        owner = people[0]
    else:
        owner = None
        for p in people:
            if last_mentioned_norm and p.lower() == last_mentioned_norm.lower():
                owner = p
                break
        if not owner:
            owner = people[0]

    # Check if owner's first word is a verb using nltk pos_tag
    first_word = owner.split()[0] if owner else ""
    pos = nltk.pos_tag([first_word])[0][1] if first_word else None

    # POS tags for verbs start with 'VB'
    if pos and pos.startswith('VB'):
        owner = "Someone"

    ambiguous = len(people) > 1
    return owner, action, ambiguous