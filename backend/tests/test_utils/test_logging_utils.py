import os
import tempfile
from app.utils import logging_utils
import pytest

def test_log_transcript_creates_file():
    test_text = "Test transcript logging"

    # Use a temporary directory to avoid polluting real folders
    with tempfile.TemporaryDirectory() as temp_dir:
        path = logging_utils.log_transcript_to_file(test_text, directory=temp_dir)
        
        # Check the returned path is inside temp_dir
        assert path.startswith(temp_dir)
        
        # Check file exists
        assert os.path.isfile(path)
        
        # Check file content matches
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        assert content == test_text

def test_log_event_creates_file(tmp_path, monkeypatch):
    # Patch 'directory' parameter to a temp location
    test_dir = tmp_path / "event_logs"
    test_dir.mkdir()
    event = {"type": "test", "msg": "Hello"}
    # Use explicit directory argument so no monkeypatching needed!
    path = logging_utils.log_event(event, directory=str(test_dir))
    assert os.path.exists(path)
    # Check that the logged event is present in the file
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    assert any('"type": "test"' in line for line in lines)

def test_log_event_handles_missing_fields(tmp_path):
    # Use explicit directory argument
    test_dir = tmp_path / "event_logs"
    test_dir.mkdir()
    # Minimal event, missing type
    logging_utils.log_event({}, directory=str(test_dir))
    # Not a dict, should still not raise
    logging_utils.log_event(None, directory=str(test_dir))
    # Confirm a log file is still created
    files = list(test_dir.glob("*.jsonl"))
    assert files, "No log file was created"

def test_log_event_with_empty_event(tmp_path):
    # Should not raise even if event is empty
    path = logging_utils.log_event({}, directory=str(tmp_path))
    assert os.path.exists(path)

def test_log_event_with_missing_fields(tmp_path):
    # Missing "type", should still log
    event = {"foo": "bar"}
    path = logging_utils.log_event(event, directory=str(tmp_path))
    assert os.path.exists(path)

def test_log_event_with_none_event(tmp_path):
    # Passing None as event
    path = logging_utils.log_event({}, directory=str(tmp_path))
    assert os.path.exists(path)

def test_log_event_unwritable_dir(monkeypatch):
    # Simulate os.makedirs raising an error
    def fail_makedirs(*a, **k): raise PermissionError("No write permission")
    monkeypatch.setattr(os, "makedirs", fail_makedirs)
    result = logging_utils.log_event({"type": "test"})
    assert result == ""

def test_log_event_open_fails(monkeypatch, tmp_path):
    # Patch open to raise an error
    def fail_open(*a, **k): raise IOError("open failed")
    monkeypatch.setattr("builtins.open", fail_open)
    result = logging_utils.log_event({"type": "test"}, directory=str(tmp_path))
    assert result == ""

def test_log_action_and_decision(tmp_path):
    logging_utils.log_action("An action", "Bob", "meetingX")
    logging_utils.log_decision("A decision", "meetingX")

def test_log_entity_extraction(tmp_path):
    logging_utils.log_entity_extraction([{"entity": "date", "value": "tomorrow"}], "meetingX")

def test_log_calendar_event(tmp_path):
    logging_utils.log_calendar_event("Title", "2024-01-01T00:00:00", owner="Sam", status="fail", meeting_id="m123")

def test_log_error_and_feedback(tmp_path):
    logging_utils.log_error("Something went wrong", details="Traceback", user="bob")
    logging_utils.log_feedback("bob", 3, comments="Not bad")

def test_log_meeting_meta_and_analytics(tmp_path):
    logging_utils.log_meeting_meta(["bob", "alice"], duration=33, filename="audio.wav", meeting_id="mid1")
    logging_utils.log_analytics_event("eventName", {"foo": "bar"})

def test_log_transcript_to_file_open_fails(monkeypatch):
    def fail_open(*a, **k): raise IOError("fail open")
    monkeypatch.setattr("builtins.open", fail_open)
    path = logging_utils.log_transcript_to_file("text", directory="testdir")
    assert path == ""
