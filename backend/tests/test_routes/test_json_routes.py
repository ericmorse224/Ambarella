import pytest
from flask import json
from app import create_app
from app.routes import json_routes
import os
import json

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

def test_process_json_invalid_content_type(client):
    resp = client.post('/process-json', data="not json", content_type="text/plain")
    assert resp.status_code == 415

def test_process_json_malformed_json(client):
    resp = client.post('/process-json', data="{bad json}", content_type="application/json")
    assert resp.status_code == 400

def test_process_json_missing_transcript(client):
    resp = client.post('/process-json', json={})
    assert resp.status_code == 400
    assert "Missing transcript" in resp.get_json().get("error", "")

def test_feedback_valid(client, tmp_path, monkeypatch):
    # Patch log_event to avoid actual file writes
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
    resp = client.post("/feedback", data="not json", content_type="text/plain")
    assert resp.status_code == 415
    assert "Invalid content type" in resp.get_json()["error"]

def test_feedback_missing_fields(client, monkeypatch):
    # Patch log_event to avoid file I/O
    monkeypatch.setattr("app.utils.logging_utils.log_event", lambda *a, **kw: None)
    payload = {}  # all fields missing
    resp = client.post("/feedback", json=payload)
    # Should still succeed, as the backend doesn't strictly require fields
    assert resp.status_code == 200

def test_feedback_log_event_error(client, monkeypatch):
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

def test_process_json_invalid_content_type(client):
    resp = client.post('/process-json', data="not json", content_type="text/plain")
    assert resp.status_code == 415
    assert "Invalid content type" in resp.get_json()["error"]

def test_process_json_malformed_json(client):
    resp = client.post('/process-json', data="{bad json}", content_type="application/json")
    assert resp.status_code == 400
    assert "Malformed JSON" in resp.get_json()["error"]

def test_process_json_missing_transcript(client):
    resp = client.post('/process-json', json={})
    assert resp.status_code == 400
    assert "Missing transcript" in resp.get_json()["error"]

def test_process_json_nlp_failure(client, monkeypatch):
    def fail_analyze(*a, **kw): raise Exception("NLP failed!")
    monkeypatch.setattr(json_routes, "analyze_transcript", fail_analyze)
    payload = {"transcript": "hello world"}
    resp = client.post('/process-json', json=payload)
    assert resp.status_code == 500
    data = resp.get_json()
    assert "NLP analysis failed" in data["error"]
    assert "NLP failed!" in data["details"]

def test_feedback_invalid_content_type(client):
    resp = client.post('/feedback', data="nope", content_type="text/plain")
    assert resp.status_code == 415
    assert "Invalid content type" in resp.get_json()["error"]

def test_feedback_success(client, monkeypatch):
    # Patch log_event to avoid file writing
    monkeypatch.setattr("app.utils.logging_utils.log_event", lambda *a, **kw: None)
    payload = {
        "meeting_id": "meetingX",
        "user": "sam",
        "score": 5,
        "comments": "Well done!"
    }
    resp = client.post('/feedback', json=payload)
    assert resp.status_code == 200
    assert resp.get_json()["success"] is True

def test_feedback_logging_error(client, monkeypatch):
    def fail_log(*a, **k): raise Exception("Logging failed intentionally")
    # Patch the correct reference (see prior answer if unsure)
    from app.routes import json_routes
    monkeypatch.setattr(json_routes, "log_event", fail_log)
    payload = {"meeting_id": "meetingX"}
    resp = client.post('/feedback', json=payload)
    assert resp.status_code == 400
    data = resp.get_json()
    assert data["success"] is False
    assert "Logging failed intentionally" in data["error"]

def test_process_json_get_method_not_allowed(client):
    resp = client.get('/process-json')
    assert resp.status_code == 405

def test_get_event_logs_for_meeting(tmp_path, monkeypatch):
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
    resp = client.post('/process-json', data="")
    # Should return 415 (invalid content type) or 400 (malformed)
    assert resp.status_code in (400, 415)

def test_process_json_missing_content_type(client):
    resp = client.post('/process-json', data="")  # No content_type set
    # Should return 415 (invalid content type)
    assert resp.status_code == 415 or resp.status_code == 400

def test_process_json_no_content_type_no_data(client):
    # No content_type and empty data triggers early error
    resp = client.post('/process-json', data="")
    assert resp.status_code in (400, 415)

def test_process_json_not_json_content_type_explicit(client):
    resp = client.post('/process-json', data='{"transcript": "hello"}', content_type="text/plain")
    assert resp.status_code == 415
    assert "Invalid content type" in resp.get_json()["error"]
