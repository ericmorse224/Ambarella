import sys
import os
import pytest
import re
import nltk

# Add project root to sys.path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.utils.entity_utils import (
    assign_owner,
    normalize_name,
    extract_entities,
    clean_name,
    extract_people_from_entities,
    assign_actions_to_people
)

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
    assert assigned[0]["owner"].lower() == "alice"
    assert assigned[1]["owner"].lower() == "charlie"
    assert assigned[2]["owner"] == "Unassigned"

def test_extract_people_with_titles():
    text = "Dr. Alice Smith and Mr. Bob Lee attended. Ms. Carol Jones presented."

    entities = extract_entities(text)
    print("Full entities:", entities)  # Debug print

    people = extract_people_from_entities(entities)
    print("Extracted people:", people)  # Debug print

    # Use normalize_name but expect capitalized (preserved) casing from your code
    normalized_people = [normalize_name(p) for p in people]

    # Normalize expected names for comparison
    expected_names = ["Alice", "Bob", "Carol"]

    # Normalize extracted to lowercase for case-insensitive compare
    extracted_lower = [p.lower() for p in normalized_people]

    for expected in expected_names:
        assert expected.lower() in extracted_lower, f"{expected} not found in extracted people"

def test_normalize_name_removes_titles():
    # Adjust expectation to preserve capitalization but remove titles
    assert normalize_name("Dr. Alice Smith") == "Alice Smith"
    assert normalize_name("Mr. Bob Lee") == "Bob Lee"
    assert normalize_name("Ms. Carol Jones") == "Carol Jones"

def test_extract_people_basic():
    text = "Alice and Bob are attending the meeting."

    entities = extract_entities(text)
    people = extract_people_from_entities(entities)
    normalized_people = [normalize_name(p) for p in people]

    # Expect Alice and Bob case-insensitive
    assert "alice" in [p.lower() for p in normalized_people]
    assert "bob" in [p.lower() for p in normalized_people]

def test_assign_owner_no_person():
    action = "Wash the car"
    entities = [{"text": "meeting", "entity_type": "ORG"}]  # No PERSON entity
    owner, mod_action, ambiguous = assign_owner(action, entities)
    assert owner == "Someone"
    assert ambiguous is True

def test_assign_owner_owner_is_verb(monkeypatch):
    action = "Go shopping"
    entities = [{"text": "Go", "entity_type": "PERSON"}]
    # Monkeypatch NLTK to tag "Go" as a verb
    monkeypatch.setattr(nltk, "pos_tag", lambda words: [("Go", "VB")])
    owner, mod_action, ambiguous = assign_owner(action, entities)
    assert owner == "Someone"

def test_assign_owner_ambiguous(monkeypatch):
    action = "Frank and Alice need to work"
    entities = [
        {"text": "Frank", "entity_type": "PERSON"},
        {"text": "Alice", "entity_type": "PERSON"}
    ]
    # Patch pos_tag to not tag as verb (simulate names)
    monkeypatch.setattr(nltk, "pos_tag", lambda words: [(w, "NNP") for w in words])
    owner, mod_action, ambiguous = assign_owner(action, entities, last_mentioned="Nonexistent")
    assert owner == "Frank"  # Falls back to first in list
    assert ambiguous is True

