import subprocess
import os
from app.utils.logger import logger

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def convert_to_wav(input_path: str, output_path: str) -> None:
    """
    Converts audio to mono WAV at 16kHz.
    """
    logger.info(f"Converting audio to WAV: {input_path} → {output_path}")
    subprocess.run(["ffmpeg", "-y", "-i", input_path, "-ac", "1", "-ar", "16000", output_path], check=True)

def trim_silence(input_path: str, output_path: str) -> bool:
    """
    Attempts to trim silence from audio using ffmpeg's silenceremove.
    Returns True if successful, False otherwise.
    """
    logger.info(f"Trimming silence from: {input_path}")
    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", input_path,
            "-af", "silenceremove=start_periods=1:start_duration=0.5:start_threshold=-50dB:"
                   "stop_periods=1:stop_duration=0.5:stop_threshold=-50dB",
            output_path
        ], check=True)
        return True
    except subprocess.CalledProcessError as e:
        logger.warning(f"Silence trimming failed: {e}")
        return False
