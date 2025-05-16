import os
from app.utils.logging_utils import log_transcript_to_file

def test_log_transcript_creates_file():
    test_text = "Test transcript logging"
    log_transcript_to_file(test_text)
    files = os.listdir("transcripts")
    assert any("transcript_" in f for f in files)