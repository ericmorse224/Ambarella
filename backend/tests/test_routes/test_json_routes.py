import pytest
from unittest.mock import patch

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
    assert "Transcript missing." in response.get_data(as_text=True)

def test_invalid_json_to_process_json(client):
    response = client.post('/process-json', json={})
    assert response.status_code == 400
    assert response.get_json()['error'] == "Transcript missing."

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
