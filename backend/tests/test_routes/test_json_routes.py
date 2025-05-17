import pytest
from flask import json
from unittest.mock import patch
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    return app.test_client()

@pytest.fixture
def app():
    from app import create_app
    return create_app()

@pytest.fixture
def client(app):
    return app.test_client()

def test_json_post_missing_transcript(client):
    response = client.post("/process-json", json={"entities": []})
    assert response.status_code == 400
    assert "Missing transcript" in response.get_data(as_text=True)

def test_invalid_json_to_process_json(client):
    response = client.post('/process-json', json={})
    assert response.status_code == 400
    assert response.get_json()['error'] == "Missing transcript"

@patch("app.utils.zoho_utils.create_calendar_event")
@patch("app.services.nlp_analysis.generate_summary_and_extraction")
def test_process_json_with_sample(mock_generate, mock_create, client):
    mock_generate.return_value = """
Summary:
- Mock summary

Action Items:
- John needs to prepare slides

Decisions:
- We are launching next week
"""
    mock_create.return_value = {"status": "success"}

    sample = {"transcript": "We decided to launch next week. John will prepare slides."}
    response = client.post('/process-json', json=sample)

    assert response.status_code == 200
    data = response.get_json()
    assert "summary" in data
    assert "actions" in data
    assert "decisions" in data

def test_process_json_valid(client, monkeypatch):
    def mock_analyze_transcript(transcript):
        return {
            "summary": ["This is a summary."],
            "actions": [{"text": "Do X"}],
            "decisions": ["Approve budget"]
        }

    monkeypatch.setattr("app.routes.json_routes.analyze_transcript", mock_analyze_transcript)

    response = client.post("/process-json", json={"transcript": "Discuss X"})
    assert response.status_code == 200


def test_process_json_missing_transcript(client):
    response = client.post("/process-json", json={})
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_process_json_malformed(client):
    response = client.post("/process-json", data="not a json", content_type="application/json")
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_process_json_analysis_error(client, mocker):
    mocker.patch("app.routes.json_routes.analyze_transcript", side_effect=Exception("LLM error"))

    response = client.post("/process-json", json={"transcript": "Bob will update."})
    assert response.status_code == 500
    assert "error" in response.get_json()
    assert "LLM error" in response.get_json()["error"]

# 1. Valid transcript input returns correct structure
@patch("app.routes.json_routes.analyze_transcript")
def test_valid_transcript(mock_analyze, client):
    mock_analyze.return_value = {
        "summary": ["Meeting summary"],
        "actions": [{"text": "Action item"}],
        "decisions": ["Decision made"]
    }
    response = client.post("/process-json", json={"transcript": "Let's do it."})
    data = response.get_json()

    assert response.status_code == 200
    assert "summary" in data
    assert "actions" in data
    assert "decisions" in data

# 2. Empty transcript input
@patch("app.routes.json_routes.analyze_transcript")
def test_empty_transcript(mock_analyze, client):
    mock_analyze.return_value = {
        "summary": [],
        "actions": [],
        "decisions": []
    }
    response = client.post("/process-json", json={"transcript": ""})
    data = response.get_json()

    assert response.status_code == 200
    assert data["summary"] == []
    assert data["actions"] == []
    assert data["decisions"] == []

def test_non_json_content_type(client):
    response = client.post("/process-json", data="not json", content_type="text/plain")
    assert response.status_code == 415
    assert "Invalid content type" in response.get_json()["error"]


# 4. JSON without transcript field
def test_json_missing_transcript(client):
    response = client.post("/process-json", json={})
    assert response.status_code == 400
    assert response.get_json()["error"] == "Missing transcript"

# 5. LLM analysis throws exception
@patch("app.routes.json_routes.analyze_transcript", side_effect=Exception("LLM error"))
def test_analysis_exception(mock_analyze, client):
    response = client.post("/process-json", json={"transcript": "something"})
    assert response.status_code == 500
    assert "LLM error" in response.get_json()["error"]

def test_malformed_json_body(client):
    response = client.post("/process-json", data="{bad json", content_type="application/json")
    assert response.status_code == 400
    assert "Malformed JSON" in response.get_json()["error"]

@patch("app.services.nlp_analysis.generate_summary_and_extraction")
def test_empty_transcript_input(mock_generate, client):
    mock_generate.return_value = {
        "summary": [],
        "actions": [],
        "decisions": []
    }
    response = client.post('/process-json', json={"transcript": ""})
    data = response.get_json()
    assert response.status_code == 200
    assert "summary" in data
    assert "actions" in data
    assert "decisions" in data

@patch("app.services.nlp_analysis.generate_summary_and_extraction")
def test_transcript_whitespace_only(mock_generate, client):
    mock_generate.return_value = "Summary:\n\nActions:\n\nDecisions:"
    response = client.post("/process-json", json={"transcript": "     "})
    assert response.status_code == 200
    assert "summary" in response.get_json()

@patch("app.services.nlp_analysis.generate_summary_and_extraction")
def test_transcript_non_english(mock_generate, client):
    mock_generate.return_value = {
        "summary": "これは要約です。",
        "actions": [],
        "decisions": []
    }
    response = client.post('/process-json', json={"transcript": "これは日本語のテキストです"})
    assert response.status_code == 200
    assert "summary" in response.get_json()

@patch("app.services.nlp_analysis.generate_summary_and_extraction")
def test_transcript_with_punctuation(mock_generate, client):
    mock_generate.return_value = {
        "summary": "Handled punctuation.",
        "actions": [],
        "decisions": []
    }
    response = client.post('/process-json', json={"transcript": "Hello... Wait--are we live?!"})
    assert response.status_code == 200
    assert "summary" in response.get_json()

@patch("app.services.nlp_analysis.generate_summary_and_extraction")
def test_transcript_with_no_actions(mock_generate, client):
    mock_generate.return_value = "Summary:\nDiscussion.\nActions:\n- Someone should follow up.\nDecisions:"
    response = client.post("/process-json", json={"transcript": "There was a vague conversation."})
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["actions"]) == 1
    assert data["actions"][0]["owner"] == "Someone"
    assert data["actions"][0]["is_ambiguous"] is True


@patch("app.services.nlp_analysis.generate_summary_and_extraction")
def test_large_transcript(mock_generate, client):
    mock_generate.return_value = {
        "summary": "Long transcript processed.",
        "actions": [],
        "decisions": []
    }
    long_text = "Repeat this sentence. " * 5000
    response = client.post('/process-json', json={"transcript": long_text})
    assert response.status_code == 200
    assert "summary" in response.get_json()


@patch("app.routes.json_routes.analyze_transcript", side_effect=ValueError("Test exception"))
def test_analyze_transcript_raises_error(mock_analyze, client):
    response = client.post('/process-json', json={"transcript": "Trigger error"})
    assert response.status_code == 500
    assert "error" in response.get_json()

def test_get_method_not_allowed(client):
    response = client.get('/process-json')
    assert response.status_code == 405