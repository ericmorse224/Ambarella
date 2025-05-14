import sys
import os
from pathlib import Path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import pytest
import tempfile
from unittest.mock import patch
from zoho_utils import refresh_access_token, save_tokens, load_tokens, load_access_token, create_calendar_event

@pytest.fixture
def temp_token_file(monkeypatch):
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        path = Path(tf.name)  # Ensure Path object
    monkeypatch.setenv("ZOHO_CLIENT_ID", "dummy_id")
    monkeypatch.setenv("ZOHO_CLIENT_SECRET", "dummy_secret")
    monkeypatch.setenv("ZOHO_REFRESH_TOKEN", "dummy_refresh")
    monkeypatch.setattr("zoho_utils.TOKENS_FILE", path)
    yield path
    os.remove(path)

@patch("requests.post")
def test_refresh_access_token_success(mock_post, temp_token_file, monkeypatch):
    # Do NOT override TOKENS_FILE again here — already handled in fixture

    mock_post.return_value.ok = True
    mock_post.return_value.json.return_value = {
        "access_token": "new_token"
    ***REMOVED***

    access_token, saved = refresh_access_token()
    assert access_token == "new_token"
    assert saved is True

    with open(temp_token_file, "r") as f:
        data = json.load(f)
        assert data["access_token"] == "new_token"

def test_load_access_token(temp_token_file, monkeypatch):
    monkeypatch.setattr("zoho_utils.TOKENS_FILE", Path(temp_token_file))

    with open(temp_token_file, "w") as f:
        json.dump({"access_token": "token_xyz"***REMOVED***, f)

    token = load_access_token()
    assert token == "token_xyz"

@patch("requests.post")
def test_refresh_access_token_failure(mock_post, temp_token_file):
    mock_post.return_value.ok = False
    with pytest.raises(Exception, match="Failed to refresh Zoho access token"):
        refresh_access_token()

def test_save_and_load_tokens(temp_token_file):
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr("zoho_utils.TOKENS_FILE", Path(temp_token_file))
    sample_data = {"access_token": "abc123", "expires_in": 3600***REMOVED***
    save_tokens(sample_data)
    loaded = load_tokens()
    assert loaded == sample_data

@patch("zoho_utils.refresh_access_token", return_value=("mock_token", True))
@patch("zoho_utils.requests.post")
def test_create_calendar_event_success(mock_post, mock_refresh_token, temp_token_file):
    mock_post.return_value.ok = True
    mock_post.return_value.json.return_value = {"event_id": "12345"***REMOVED***

    response = create_calendar_event(
        title="Test Event",
        description="This is a test.",
        start_time="2025-05-13T10:00:00Z",
        end_time="2025-05-13T10:30:00Z"
    )
    assert "event_id" in response

@patch("pathlib.Path.chmod", side_effect=PermissionError("Permission denied"))
def test_save_tokens_permission_error(mock_chmod, temp_token_file):
    sample_data = {"access_token": "abc123"***REMOVED***
    # This should trigger the internal try/except in save_tokens()
    save_tokens(sample_data)
    # No assert needed — we're just testing that the error is caught and logged


@patch("requests.post")
def test_refresh_expired_token(mock_post, temp_token_file, monkeypatch):
    monkeypatch.setenv("ZOHO_CLIENT_ID", "dummy_id")
    monkeypatch.setenv("ZOHO_CLIENT_SECRET", "dummy_secret")
    monkeypatch.setenv("ZOHO_REFRESH_TOKEN", "dummy_refresh")

    mock_post.return_value.ok = True
    mock_post.return_value.json.return_value = {
        "access_token": "expired_token",
        "expires_in": 0
    ***REMOVED***

    access_token, saved = refresh_access_token()
    assert access_token == "expired_token"
    assert saved is True
