import sys
import os
import pytest
import re

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
    "action, entities, last_mentioned, expected_owner, expected_ambiguous, expected_contains",
    [
        (
            "Dr. Bob should finalize slides.",
            [{"text": "Dr. Bob", "entity_type": "PERSON"}],
            None,
            "Bob",
            False,
            "Dr. Bob should finalize slides."  # Preserve original text casing including titles
        ),
        (
            "Charlie and Alice need to check data.",
            [
                {"text": "Charlie", "entity_type": "PERSON"},
                {"text": "Alice", "entity_type": "PERSON"},
            ],
            None,
            "Charlie",
            False,
            "Charlie and Alice need to check data."
        ),
        (
            "Someone must fix this bug.",
            [],
            None,
            "Someone",
            True,
            "Someone must fix this bug."
        ),
        (
            "He will review it.",
            [],
            "Alice",
            "Alice",
            False,
            "He will review it."
        ),
        (
            "Alice will prepare the report.",
            [{"text": "Alice", "entity_type": "PERSON"}],
            None,
            "Alice",
            False,
            "Alice will prepare the report."
        ),
    ],
)
def test_assign_owner(action, entities, last_mentioned, expected_owner, expected_ambiguous, expected_contains):
    owner, assigned_action, is_ambiguous = assign_owner(action, entities, last_mentioned)
    # Normalize owner for case-insensitive comparison
    assert normalize_name(owner) == expected_owner
    assert is_ambiguous == expected_ambiguous
    # Case insensitive check for assigned action containing expected text
    assert expected_contains.lower() in assigned_action.lower()

def test_assign_actions_to_people_case_insensitive():
    actions = ["alice will prepare notes", "Charlie will call", "Someone needs to summarize"]
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
