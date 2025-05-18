import sys
import os

# Add project base directory to sys.path to ensure all imports work correctly
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


import pytest
from app.services.nlp_analysis import analyze_transcript

def test_analyze_transcript_exists():
    result = analyze_transcript("Bob will prepare the slides. Alice will follow up.")
    assert "summary" in result and isinstance(result["summary"], list)
    assert "actions" in result and isinstance(result["actions"], list)
    assert "decisions" in result and isinstance(result["decisions"], list)

def test_analyze_transcript_structure():
    result = analyze_transcript("Some summary here.")
    assert isinstance(result["summary"], list)
    assert isinstance(result["actions"], list)
    assert isinstance(result["decisions"], list)

def test_analyze_transcript_action_assignment():
    result = analyze_transcript("Bob will finalize the slides.")
    actions = result["actions"]
    if actions:
        # Check at least one action owner includes 'Bob' (case-insensitive)
        assert any("bob" in (a.get("owner", "").lower()) for a in actions)

def test_empty_transcript_returns_empty_sections():
    result = analyze_transcript("")
    assert result["summary"] == []
    assert result["actions"] == []
    assert result["decisions"] == []

def test_transcript_with_no_actions():
    result = analyze_transcript("This meeting was only a general discussion.")
    # actions can be empty or a list; ensure it does not error
    assert isinstance(result["actions"], list)

def test_transcript_with_ambiguous_actions():
    transcript = "Update the roadmap. Send out the schedule."
    result = analyze_transcript(transcript)
    actions = result["actions"]
    assert isinstance(actions, list)
    assert len(actions) >= 2
    assert all("text" in a for a in actions)

def test_owner_fallback_behavior():
    transcript = "Finalize the report. Summarize findings."
    result = analyze_transcript(transcript)
    actions = result["actions"]
    if actions:
        # When no specific person, owner should be "Unassigned"
        assert all(a.get("owner", "Unassigned") == "Unassigned" for a in actions)
