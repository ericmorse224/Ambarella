import sys
import os
import pytest
import re
from app.utils.entity_utils import assign_owner, normalize_name, extract_entities, clean_name, extract_people_from_entities, extract_probable_people

# Add project root to sys.path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.utils.entity_utils import (
    extract_entities,
    extract_people_from_entities,
    assign_actions_to_people,
    assign_owner
)

def normalize_name(name: str) -> str:
    # Remove titles and capitalize each word (Title Case)
    name_no_title = re.sub(r'\b(Mr|Ms|Mrs|Dr|Prof|Sir|Madam)\.? ', '', name, flags=re.I)
    return name_no_title.title()

@pytest.mark.parametrize(
    "action_text, entities, last_mentioned, expected_owner, expected_ambiguous, expected_action_substr",
    [
        (
            "Alice will prepare the report.",
            [{"text": "Alice", "entity_type": "PERSON"}],
            None,
            "Alice",
            False,
            "Alice will prepare the report."
        ),
        (
            "Dr. Bob should finalize slides.",
            [{"text": "Dr. Bob", "entity_type": "PERSON"}],
            None,
            "Bob",
            False,
            "Dr. Bob should finalize slides."
        ),
        (
            "Charlie and Alice need to check data.",
            [
                {"text": "Charlie", "entity_type": "PERSON"},
                {"text": "Alice", "entity_type": "PERSON"}
            ],
            None,
            "Charlie",
            True,
            "Charlie and Alice need to check data."
        ),
        (
            "He will review it.",
            [{"text": "Alice", "entity_type": "PERSON"}],
            "Alice",
            "Alice",
            False,
            "He will review it."
        ),
        (
            "Someone must fix this bug.",
            [],
            None,
            "Someone",
            True,
            "Someone must fix this bug."
        )
    ]
)
def test_assign_owner(action_text, entities, last_mentioned, expected_owner, expected_ambiguous, expected_action_substr):
    owner, modified_action, is_ambiguous = assign_owner(action_text, entities, last_mentioned)

    # Normalize owner names for comparison using main code function
    owner_norm = normalize_name(owner)
    expected_owner_norm = normalize_name(expected_owner)

    assert owner_norm == expected_owner_norm, (
        f"Owner mismatch: expected '{expected_owner}', got '{owner}'."
    )
    assert is_ambiguous == expected_ambiguous, (
        f"Ambiguity flag mismatch for owner '{owner}': expected {expected_ambiguous}, got {is_ambiguous}."
    )
    assert expected_action_substr.lower() in modified_action.lower(), (
        f"Action text mismatch: expected substring '{expected_action_substr}' in '{modified_action}'."
    )

def test_assign_actions_to_people_case_insensitive():
    actions = ["Alice will prepare notes", "Charlie will call", "Someone needs to summarize"]
    people = ["Alice", "Charlie"]
    assigned = assign_actions_to_people(actions, people)
    assert assigned[0]["owner"] == "Alice"
    assert assigned[1]["owner"] == "Charlie"
    assert assigned[2]["owner"] == "Unassigned"

def test_extract_people_with_titles():
    text = "Dr. Alice Smith and Mr. Bob Lee attended. Ms. Carol Jones presented."
    entities = extract_entities(text)
    people = extract_people_from_entities(entities)

    found_alice = any("alice" in name.lower() for name in people)
    found_bob = any("bob" in name.lower() for name in people)
    found_carol = any("carol" in name.lower() for name in people)

    print("Extracted people:", people)

    assert found_alice, "Alice not found in extracted people"
    assert found_bob, "Bob not found in extracted people"
    assert found_carol, "Carol not found in extracted people"
