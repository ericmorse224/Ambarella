from app.utils.entity_utils import extract_people, assign_actions_to_people

def test_extract_people_basic():
    text = "Alice and Bob will join. Charlie should present."
    people = extract_people(text)
    assert "Alice" in people and "Bob" in people

def test_assign_actions_to_people_case_insensitive():
    actions = ["alice will prepare notes", "Charlie will call"]
    people = ["Alice", "Charlie"]
    assigned = assign_actions_to_people(actions, people)
    assert assigned[0]["owner"] == "Alice"
    assert assigned[1]["owner"] == "Charlie"