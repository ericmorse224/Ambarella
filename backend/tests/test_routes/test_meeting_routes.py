import os
import json
import pytest
from unittest.mock import patch, mock_open
from flask import Flask
from app.routes.meeting_routes import dashboard_bp

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(dashboard_bp)
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_get_meeting_meta_logs_success(client):
    mock_lines = [
        json.dumps({"type": "meeting_meta", "logged_at": "2025-05-17T12:00:00Z", "data": "entry1"}) + "\n",
        json.dumps({"type": "other_type", "logged_at": "2025-05-17T12:01:00Z", "data": "entry2"}) + "\n",
        json.dumps({"type": "meeting_meta", "logged_at": "2025-05-17T11:59:00Z", "data": "entry3"}) + "\n",
        "bad json line\n"
    ]
    mock_files = ["event_log_2025-05-17.jsonl"]

    def mock_isdir(path):
        return True

    def mock_listdir(path):
        return mock_files

    m_open = mock_open(read_data="".join(mock_lines))

    with patch("os.path.isdir", mock_isdir), \
         patch("os.listdir", mock_listdir), \
         patch("builtins.open", m_open), \
         patch("app.routes.meeting_routes.log_event") as mock_log_event:

        resp = client.get("/api/meetings/meta")
        data = resp.get_json()

        assert resp.status_code == 200
        assert isinstance(data, dict)
        assert "logs" in data
        assert "skipped_lines" in data
        assert "skipped_files" in data

        assert all(entry["type"] == "meeting_meta" for entry in data["logs"])
        assert len(data["logs"]) == 2
        assert data["logs"][0]["logged_at"] >= data["logs"][1]["logged_at"]
        assert data["skipped_lines"] == 1
        assert "event_log_2025-05-17.jsonl" in data["skipped_files"]
        mock_log_event.assert_called()

def test_get_meeting_meta_logs_no_directory(client):
    with patch("os.path.isdir", return_value=False):
        resp = client.get("/api/meetings/meta")
        data = resp.get_json()

        assert resp.status_code == 200
        assert data == {"logs": [], "skipped_lines": 0, "skipped_files": []}

def test_get_meeting_meta_logs_file_open_error(client):
    mock_files = ["event_log_2025-05-17.jsonl"]

    def mock_isdir(path):
        return True

    def mock_listdir(path):
        return mock_files

    def mock_open_fail(*args, **kwargs):
        raise IOError("Permission denied")

    with patch("os.path.isdir", mock_isdir), \
         patch("os.listdir", mock_listdir), \
         patch("builtins.open", mock_open_fail), \
         patch("app.routes.meeting_routes.log_event") as mock_log_event:

        resp = client.get("/api/meetings/meta")
        data = resp.get_json()

        assert resp.status_code == 200
        assert data["logs"] == []
        assert data["skipped_lines"] == 0
        assert "event_log_2025-05-17.jsonl" in data["skipped_files"]
        mock_log_event.assert_called()

def test_get_meeting_meta_logs_json_decode_error(client):
    mock_lines = [
        "not a json\n",
        '{"type": "meeting_meta", "logged_at": "2025-05-17T12:00:00Z"}\n',
        "bad json again\n"
    ]
    mock_files = ["event_log_2025-05-17.jsonl"]

    def mock_isdir(path):
        return True

    def mock_listdir(path):
        return mock_files

    m_open = mock_open(read_data="".join(mock_lines))

    with patch("os.path.isdir", mock_isdir), \
         patch("os.listdir", mock_listdir), \
         patch("builtins.open", m_open), \
         patch("app.routes.meeting_routes.log_event") as mock_log_event:

        resp = client.get("/api/meetings/meta")
        data = resp.get_json()

        assert resp.status_code == 200
        assert any("meeting_meta" == entry.get("type") for entry in data["logs"])
        assert data["skipped_lines"] >= 2
        assert "event_log_2025-05-17.jsonl" in data["skipped_files"]
        mock_log_event.assert_called()
