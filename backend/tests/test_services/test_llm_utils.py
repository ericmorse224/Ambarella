import pytest
from unittest.mock import patch
from app.services.nlp_analysis import analyze_transcript

mock_llm_output = """Summary:
- Summary line
Action Items:
- John to review docs
Decisions:
- Proceed with next steps
"""

@patch("app.services.nlp_analysis.generate_summary_and_extraction", return_value=mock_llm_output)
@pytest.mark.parametrize("transcript", [
    "Bob will prepare slides. Alice will review.",
    "No decisions were made. Tom will follow up.",
    "Someone must document this."
])
def test_llm_analysis_with_mock(mock_generate, transcript):
    result = analyze_transcript(transcript)
    assert "summary" in result
    assert "actions" in result
    assert "decisions" in result