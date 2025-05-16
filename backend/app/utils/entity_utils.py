import re

def extract_people(transcript):
    """
    Extract capitalized words that appear to be names.
    Ignores common non-name words by using a basic exclusion list.
    """
    common_words = {
        "The", "This", "That", "He", "She", "It", "They", "We", "You", "I",
        "Needs", "Should", "Will", "Must", "Decision", "Meeting", "Follow", "Up"
    }
    words = re.findall(r'\b[A-Z][a-z]{2,}\b', transcript)
    people = [word for word in set(words) if word not in common_words]
    return people

def extract_people_from_entities(entities):
    """
    Extracts names of people from detected entities with type 'person'.
    """
    return list(set(e['text'] for e in entities if e.get('entity_type') == 'person'))

def assign_actions_to_people(actions, people):
    """
    Assigns each action to a person whose name is mentioned in the action.
    """
    assigned = []
    for action in actions:
        owner = next((p for p in people if p.lower() in action.lower()), "Unassigned")
        assigned.append({"text": action, "owner": owner})
    return assigned

def assign_owner(action, entities, last_mentioned=None):
    """
    Heuristic assignment of an owner to an action item.
    Supports fallback to pronouns and generic 'Someone' if ambiguous.
    """
    person_entities = [e.lower() for e in entities]
    pronouns = {
        "he": last_mentioned,
        "she": last_mentioned,
        "they": last_mentioned
    }

    lower_action = action.lower()
    is_ambiguous = False

    for person in person_entities:
        if person in lower_action:
            cleaned_action = action.replace(person, '').strip()
            assigned = f"{person.title()} needs to {cleaned_action}"
            return person.title(), assigned, is_ambiguous

    for pronoun, fallback in pronouns.items():
        if pronoun in lower_action and fallback:
            assigned = f"{fallback.title()} needs to {action}"
            return fallback.title(), assigned, is_ambiguous

    # Fallback
    assigned = f"Someone needs to {action}"
    is_ambiguous = True

    generic_verbs = ["do", "handle", "fix", "work", "make", "take care", "something"]
    if any(word in lower_action for word in generic_verbs) or len(action.split()) < 3:
        is_ambiguous = True

    return "Someone", assigned, is_ambiguous
