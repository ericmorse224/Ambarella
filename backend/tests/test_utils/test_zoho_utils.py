import os
import json
import pytest
import tempfile
from unittest.mock import patch
from pathlib import Path

from app.utils.zoho_utils import (
    refresh_access_token,
    save_tokens,
    load_tokens,
    load_access_token,
    create_calendar_event,
)

@pytest.fixture
def temp_token_file(monkeypatch):
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        path = Path(tf.name)
    with open(path, "w") as f:
        json.dump({"access_token": "test", "refresh_token": "test"}, f)

    monkeypatch.setattr("app.utils.zoho_utils.TOKENS_FILE", path)
    yield path
    path.unlink(missing_ok=True)

def test_save_and_load_tokens(temp_token_file):
    tokens = {"access_token": "abc", "refresh_token": "def"}
    save_tokens(tokens)
    loaded = load_tokens()
    assert loaded == tokens

def test_load_access_token(temp_token_file):
    with open(temp_token_file, "w") as f:
        json.dump({"access_token": "abc"}, f)
    assert load_access_token() == "abc"

@patch("app.utils.zoho_utils.requests.post")
def test_refresh_access_token_success(mock_post, temp_token_file, monkeypatch):
    mock_post.return_value.ok = True
    mock_post.return_value.json.return_value = {
        "access_token": "new_token"
    }

    access_token = refresh_access_token()
    assert access_token == "new_token"

@patch("app.utils.zoho_utils.requests.post")
def test_refresh_access_token_failure(mock_post, temp_token_file):
    mock_post.return_value.ok = False
    with pytest.raises(Exception, match="Failed to refresh Zoho access token"):
        refresh_access_token()

@patch("app.utils.zoho_utils.make_authorized_request")
def test_create_calendar_event_success(mock_request, temp_token_file):
    mock_request.return_value.ok = True
    mock_request.return_value.json.return_value = {"event_id": "12345"}

    response = create_calendar_event(
        title="Test Event",
        description="This is a test.",
        start_time="2025-05-13T10:00:00Z",
        end_time="2025-05-13T10:30:00Z"
    )
    assert response["event_id"] == "12345"

@patch("app.utils.zoho_utils.requests.post")
def test_refresh_expired_token(mock_post, temp_token_file, monkeypatch):
    monkeypatch.setenv("ZOHO_CLIENT_ID", "dummy_id")
    monkeypatch.setenv("ZOHO_CLIENT_SECRET", "dummy_secret")
    monkeypatch.setenv("ZOHO_REFRESH_TOKEN", "dummy_refresh")

    mock_post.return_value.ok = True
    mock_post.return_value.json.return_value = {
        "access_token": "expired_token",
        "expires_in": 0
    }

    access_token = refresh_access_token()
    assert access_token == "expired_token"
