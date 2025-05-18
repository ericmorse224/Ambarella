import os
import tempfile
from app.utils.logging_utils import log_transcript_to_file

def test_log_transcript_creates_file():
    test_text = "Test transcript logging"

    # Use a temporary directory to avoid polluting real folders
    with tempfile.TemporaryDirectory() as temp_dir:
        path = log_transcript_to_file(test_text, directory=temp_dir)
        
        # Check the returned path is inside temp_dir
        assert path.startswith(temp_dir)
        
        # Check file exists
        assert os.path.isfile(path)
        
        # Check file content matches
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        assert content == test_text
