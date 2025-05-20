"""
test_json_routes.py

Unit tests for the JSON-based NLP and feedback routes in the AI Meeting Summarizer backend.

Covers:
- /process-json: Meeting transcript processing (NLP).
- /feedback: User feedback and logging.
- Error handling for malformed requests, invalid JSON, missing fields, content types, and HTTP method restrictions.
- Event log retrieval utilities.

Author: Eric Morse
Date: 2024-05-18
"""

import pytest
from flask import json
from app import create_app
from app.routes import json_routes
import os
import json

@pytest.fixture
def app():
    """
    Pytest fixture to create and configure the Flask app instance for testing.
    """
    return create_app()

@pytest.fixture
def client(app):
    """
    Pytest fixture to provide a test client for sending HTTP requests to the Flask app.
    """
    return app.test_client()

def test_json_post_missing_transcript(client):
    """
    POST /process-json with missing transcript key should return 400 error and appropriate message.
    """
    response = client.post("/process-json", json={"entities": []})
    assert response.status_code == 400
    assert "Missing transcript" in response.get_data(as_text=True)

def test_invalid_json_to_process_json(client):
    """
    POST /process-json with an empty JSON body should return 400 and missing transcript error.
    """
    response = client.post('/process-json', json={})
    assert response.status_code == 400
    assert response.get_json()['error'] == "Missing transcript"

def test_process_json_missing_transcript(client):
    """
    POST /process-json with an empty JSON should return a 400 error.
    """
    response = client.post("/process-json", json={})
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_process_json_malformed(client):
    """
    POST /process-json with malformed JSON should return 400 error.
    """
    response = client.post("/process-json", data="not a json", content_type="application/json")
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_malformed_json_body(client):
    """
    POST /process-json with syntactically invalid JSON should return 400 and indicate 'Malformed JSON'.
    """
    response = client.post("/process-json", data="{bad json", content_type="application/json")
    assert response.status_code == 400
    assert "Malformed JSON" in response.get_json()["error"]

def test_non_json_content_type(client):
    """
    POST /process-json with non-JSON content-type should return 415 error.
    """
    response = client.post("/process-json", data="not json", content_type="text/plain")
    assert response.status_code == 415
    assert "Invalid content type" in response.get_json()["error"]

def test_get_method_not_allowed(client):
    """
    GET /process-json should return 405 (method not allowed).
    """
    response = client.get('/process-json')
    assert response.status_code == 405

def test_process_json_valid_transcript(client):
    """
    POST /process-json with a valid transcript should return NLP pipeline output with expected fields.
    """
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
    """
    POST /process-json with an empty transcript should return 400.
    """
    response = client.post("/process-json", json={"transcript": ""})
    data = response.get_json()
    assert response.status_code == 400

def test_process_json_large_transcript(client):
    """
    POST /process-json with a large transcript should still return 200 and a summary.
    """
    long_text = "Discuss quarterly results. " * 1000
    response = client.post('/process-json', json={"transcript": long_text})
    assert response.status_code == 200
    data = response.get_json()
    assert "summary" in data

def test_process_json_with_actions_and_decisions(client):
    """
    POST /process-json with a transcript containing actions and a decision.
    Checks that actions/owners and decisions are parsed.
    """
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

def test_process_json_invalid_content_type(client):
    """
    POST /process-json with wrong content-type returns 415.
    """
    resp = client.post('/process-json', data="not json", content_type="text/plain")
    assert resp.status_code == 415

def test_process_json_malformed_json(client):
    """
    POST /process-json with bad JSON returns 400.
    """
    resp = client.post('/process-json', data="{bad json}", content_type="application/json")
    assert resp.status_code == 400

def test_process_json_missing_transcript(client):
    """
    POST /process-json with missing transcript returns 400 and error.
    """
    resp = client.post('/process-json', json={})
    assert resp.status_code == 400
    assert "Missing transcript" in resp.get_json().get("error", "")

def test_feedback_valid(client, tmp_path, monkeypatch):
    """
    POST /feedback with valid payload should succeed, log_event is patched to prevent I/O.
    """
    monkeypatch.setattr("app.utils.logging_utils.log_event", lambda *a, **kw: None)
    payload = {
        "meeting_id": "meeting123",
        "user": "bob",
        "score": 5,
        "comments": "Great summary!"
    }
    resp = client.post("/feedback", json=payload)
    assert resp.status_code == 200
    assert resp.get_json()["success"] is True

def test_feedback_non_json_content_type(client):
    """
    POST /feedback with non-JSON content-type returns 415.
    """
    resp = client.post("/feedback", data="not json", content_type="text/plain")
    assert resp.status_code == 415
    assert "Invalid content type" in resp.get_json()["error"]

def test_feedback_missing_fields(client, monkeypatch):
    """
    POST /feedback with missing fields still succeeds (backend doesn't require them).
    """
    monkeypatch.setattr("app.utils.logging_utils.log_event", lambda *a, **kw: None)
    payload = {}  # all fields missing
    resp = client.post("/feedback", json=payload)
    assert resp.status_code == 200

def test_feedback_log_event_error(client, monkeypatch):
    """
    POST /feedback with a log_event error returns 400 and error in response.
    """
    def fail_log_event(*a, **kw): raise Exception("Logging failed")
    monkeypatch.setattr(json_routes, "log_event", fail_log_event)
    payload = {
        "meeting_id": "meeting123",
        "user": "alice",
        "score": 3,
        "comments": "Buggy"
    }
    resp = client.post("/feedback", json=payload)
    assert resp.status_code == 400
    data = resp.get_json()
    assert data["success"] is False
    assert "Logging failed" in data["error"]

def test_process_json_nlp_failure(client, monkeypatch):
    """
    POST /process-json with NLP analysis failure returns 500 and details.
    """
    def fail_analyze(*a, **kw): raise Exception("NLP failed!")
    monkeypatch.setattr(json_routes, "analyze_transcript", fail_analyze)
    payload = {"transcript": "hello world"}
    resp = client.post('/process-json', json=payload)
    assert resp.status_code == 500
    data = resp.get_json()
    assert "NLP analysis failed" in data["error"]
    assert "NLP failed!" in data["details"]

def test_get_event_logs_for_meeting(tmp_path, monkeypatch):
    """
    Unit test for get_event_logs_for_meeting utility.
    Creates a fake log file and checks log retrieval by meeting_id.
    """
    from app.routes.json_routes import get_event_logs_for_meeting
    # Create temp event_logs dir and file
    event_logs_dir = tmp_path / "event_logs"
    event_logs_dir.mkdir()
    sample_entry = {"meeting_id": "abc", "user": "bob"}
    log_file = event_logs_dir / "log.jsonl"
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(json.dumps(sample_entry) + "\n")
        f.write("not json\n")
        f.write(json.dumps({"meeting_id": "zzz", "user": "eve"}) + "\n")
    monkeypatch.chdir(tmp_path)
    logs = get_event_logs_for_meeting("abc")
    assert isinstance(logs, list)
    assert any(entry.get("user") == "bob" for entry in logs)
    assert not get_event_logs_for_meeting("no-match")

def test_process_json_empty_post(client):
    """
    POST /process-json with empty body returns 415 (invalid content type) or 400.
    """
    resp = client.post('/process-json', data="")
    assert resp.status_code in (400, 415)

def test_process_json_missing_content_type(client):
    """
    POST /process-json with missing content-type returns 415 or 400.
    """
    resp = client.post('/process-json', data="")
    assert resp.status_code == 415 or resp.status_code == 400

def test_process_json_no_content_type_no_data(client):
    """
    POST /process-json with no content-type and empty data triggers early error.
    """
    resp = client.post('/process-json', data="")
    assert resp.status_code in (400, 415)

def test_process_json_not_json_content_type_explicit(client):
    """
    POST /process-json with valid JSON data but wrong content-type returns 415.
    """
    resp = client.post('/process-json', data='{"transcript": "hello"}', content_type="text/plain")
    assert resp.status_code == 415
    assert "Invalid content type" in resp.get_json()["error"]
