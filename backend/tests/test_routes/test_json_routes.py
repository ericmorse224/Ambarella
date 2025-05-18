import pytest
from flask import json
from app import create_app

@pytest.fixture
def app():
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

def test_process_json_missing_transcript(client):
    response = client.post("/process-json", json={})
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_process_json_malformed(client):
    response = client.post("/process-json", data="not a json", content_type="application/json")
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_malformed_json_body(client):
    response = client.post("/process-json", data="{bad json", content_type="application/json")
    assert response.status_code == 400
    assert "Malformed JSON" in response.get_json()["error"]

def test_non_json_content_type(client):
    response = client.post("/process-json", data="not json", content_type="text/plain")
    assert response.status_code == 415
    assert "Invalid content type" in response.get_json()["error"]

def test_get_method_not_allowed(client):
    response = client.get('/process-json')
    assert response.status_code == 405

def test_process_json_valid_transcript(client):
    # This tests a real transcript processed by your pipeline (NLP/Whisper/NTLK)
    sample = {"transcript": "Bob will prepare the slides. Alice will follow up. No decisions made."}
    response = client.post('/process-json', json=sample)
    assert response.status_code == 200
    data = response.get_json()
    assert "summary" in data
    assert "actions" in data
    assert "decisions" in data
    assert isinstance(data["summary"], list)
    assert isinstance(data["actions"], list)
    assert isinstance(data["decisions"], list)

def test_process_json_empty_transcript(client):
    response = client.post("/process-json", json={"transcript": ""})
    data = response.get_json()
    assert response.status_code == 400

def test_process_json_large_transcript(client):
    long_text = "Discuss quarterly results. " * 1000
    response = client.post('/process-json', json={"transcript": long_text})
    assert response.status_code == 200
    data = response.get_json()
    assert "summary" in data

def test_process_json_with_actions_and_decisions(client):
    payload = {
        "transcript": "Bob will schedule a follow-up meeting. Alice should prepare the agenda. Decision: We will adopt the new process."
    }
    response = client.post("/process-json", json=payload)
    assert response.status_code == 200

    data = response.get_json()
    print("Full response JSON:", data)

    assert "actions" in data
    assert "decisions" in data

    print("Actions extracted:", data["actions"])
    print("Owners extracted:", [a.get("owner") for a in data["actions"]])

    assert any(
        "decision" in d.get("text", "").lower() or "adopt" in d.get("text", "").lower()
        for d in data["decisions"]
    )

    assert any(
        "alice" in (a.get("owner", "") or "").lower()
        for a in data["actions"]
    )
