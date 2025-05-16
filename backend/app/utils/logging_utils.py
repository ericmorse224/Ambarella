import os
from datetime import datetime
from app.utils.logger import logger

def log_transcript_to_file(transcript: str):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs("transcripts", exist_ok=True)
    path = os.path.join("transcripts", f"transcript_{timestamp}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(transcript)
    logger.info(f"Transcript logged to {path}")
