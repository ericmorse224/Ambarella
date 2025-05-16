import pytest
from unittest.mock import patch
from app.services.nlp_analysis import analyze_transcript

@patch("app.services.nlp_analysis.generate_summary_and_extraction", return_value="""
Summary:
- Kickoff complete

Actions:
- Bob: Finalize architecture
- Alice: Collect team feedback

Decisions:
- Proceed with Plan A
""")
def test_analyze_transcript_exists(mock_llm):
    result = analyze_transcript("Bob will prepare the slides. Alice will follow up.")
    assert "summary" in result
    assert isinstance(result["summary"], str)

@patch("app.services.nlp_analysis.generate_summary_and_extraction", return_value="""
Summary:
- Review completed

Actions:
- Bob: Finalize architecture
- Tom: Document key risks

Decisions:
- Adopt hybrid approach
""")
def test_analyze_transcript_structure(mock_llm):
    result = analyze_transcript("Some summary here.")
    assert isinstance(result["summary"], str)
    assert isinstance(result["actions"], list)
    assert isinstance(result["decisions"], list)

@patch("app.services.nlp_analysis.parse_llm_sections")
@patch("app.services.nlp_analysis.generate_summary_and_extraction")
def test_analyze_transcript_action_assignment(mock_llm, mock_parse):
    mock_llm.return_value = "mocked raw output"
    mock_parse.return_value = {
        "summary": ["Reviewed roadmap."],
        "actions": [{"text": "Bob will finalize the slides."}],
        "decisions": []
    }
    result = analyze_transcript("Bob will finalize the slides.")
    actions = result["actions"]
    assert any("Bob" in a.get("owner", "") for a in actions)

@patch("app.services.nlp_analysis.parse_llm_sections")
@patch("app.services.nlp_analysis.generate_summary_and_extraction")
def test_empty_transcript_returns_empty_sections(mock_llm, mock_parse):
    mock_llm.return_value = ""
    mock_parse.return_value = {
        "summary": "",
        "actions": [],
        "decisions": []
    }
    result = analyze_transcript("")
    assert result["summary"] == ""
    assert result["actions"] == []
    assert result["decisions"] == []

@patch("app.services.nlp_analysis.parse_llm_sections")
@patch("app.services.nlp_analysis.generate_summary_and_extraction")
def test_transcript_with_no_actions(mock_llm, mock_parse):
    mock_llm.return_value = "mocked raw output"
    mock_parse.return_value = {
        "summary": ["Meeting about strategy."],
        "actions": [],
        "decisions": ["No clear next steps."]
    }
    result = analyze_transcript("Just general discussion.")
    assert result["actions"] == []

@patch("app.services.nlp_analysis.parse_llm_sections")
@patch("app.services.nlp_analysis.generate_summary_and_extraction")
def test_transcript_with_ambiguous_actions(mock_llm, mock_parse):
    mock_llm.return_value = "mocked raw output"
    mock_parse.return_value = {
        "summary": ["Ambiguous tasks assigned."],
        "actions": [
            {"text": "Update the roadmap.", "owner": "Tom", "assignment": "Update the roadmap."},
            {"text": "Send out the schedule.", "owner": "Alice", "assignment": "Send out the schedule."}
        ],
        "decisions": []
    }
    result = analyze_transcript("Tasks were not clearly assigned.")
    actions = result["actions"]
    assert len(actions) == 2
    assert all("owner" in a and a["owner"] != "" for a in actions)

@patch("app.services.nlp_analysis.parse_llm_sections")
@patch("app.services.nlp_analysis.generate_summary_and_extraction")
def test_owner_fallback_behavior(mock_llm, mock_parse):
    mock_llm.return_value = "mocked raw output"
    mock_parse.return_value = {
        "summary": ["Planning vague responsibilities."],
        "actions": [
            {"text": "Finalize the report.", "owner": "Unassigned", "assignment": "Finalize the report."},
            {"text": "Summarize findings.", "owner": "Unassigned", "assignment": "Summarize findings."}
        ],
        "decisions": []
    }
    result = analyze_transcript("Tasks were discussed vaguely.")
    actions = result["actions"]
    assert len(actions) >= 2
    assert all("owner" in a for a in actions)
