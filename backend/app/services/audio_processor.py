import subprocess
import os
from app.utils.logger import logger

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

SUPPORTED_FORMATS = {'.wav', '.mp3', '.m4a', '.aac', '.flac', '.ogg'}

def is_supported_format(path: str) -> bool:
    _, ext = os.path.splitext(path)
    return ext.lower() in SUPPORTED_FORMATS

def get_audio_duration(path: str) -> float:
    """
    Returns duration of audio in seconds or -1 on error.
    """
    try:
        result = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries",
            "format=duration", "-of",
            "default=noprint_wrappers=1:nokey=1", path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return float(result.stdout.strip())
    except Exception as e:
        logger.warning(f"Failed to get duration for {path}: {e}")
        return -1

def get_sample_rate_channels(path: str):
    """
    Returns sample rate and number of channels or (0, 0) on error.
    """
    try:
        result = subprocess.run([
            "ffprobe", "-v", "error",
            "-select_streams", "a:0",
            "-show_entries", "stream=sample_rate,channels",
            "-of", "default=noprint_wrappers=1:nokey=1", path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        lines = result.stdout.strip().split('\n')
        sample_rate = int(lines[0]) if len(lines) > 0 else 0
        channels = int(lines[1]) if len(lines) > 1 else 0
        return sample_rate, channels
    except Exception as e:
        logger.warning(f"Failed to get sample rate/channels for {path}: {e}")
        return 0, 0

def get_bitrate(path: str) -> int:
    """
    Returns bitrate in bps or 0 on error.
    """
    try:
        result = subprocess.run([
            "ffprobe", "-v", "error",
            "-select_streams", "a:0",
            "-show_entries", "format=bit_rate",
            "-of", "default=noprint_wrappers=1:nokey=1", path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return int(result.stdout.strip())
    except Exception as e:
        logger.warning(f"Failed to get bitrate for {path}: {e}")
        return 0

def get_rms_volume(path: str) -> float | None:
    """
    Uses ffmpeg's volumedetect filter to get mean RMS volume in dB.
    Returns dB float or None if failed.
    """
    try:
        proc = subprocess.run([
            "ffmpeg", "-i", path, "-af", "volumedetect", "-f", "null", "-"
        ], stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, check=True)
        lines = proc.stderr.splitlines()
        for line in lines:
            if "mean_volume:" in line:
                # line example: [Parsed_volumedetect_0 @ 000001f0c0a4e840] mean_volume: -26.0 dB
                parts = line.strip().split()
                for i, part in enumerate(parts):
                    if part == "mean_volume:" and i + 1 < len(parts):
                        val = parts[i+1]
                        if val.endswith("dB"):
                            return float(val[:-2])
                        else:
                            return float(val)
        return None
    except Exception as e:
        logger.warning(f"Failed to get RMS volume for {path}: {e}")
        return None

def get_silence_ratio(path: str, silence_threshold_db: float = -50.0) -> float:
    """
    Estimate ratio of silence in audio by counting silent segments using ffmpeg's silencedetect.
    Returns ratio 0.0-1.0 or 1.0 if error.
    """
    try:
        # Run ffmpeg silencedetect filter
        proc = subprocess.run([
            "ffmpeg", "-i", path,
            "-af", f"silencedetect=noise={silence_threshold_db}dB:d=0.5",
            "-f", "null", "-"
        ], stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, check=True)
        output = proc.stderr

        # Parse silence start/end times
        silence_durations = []
        current_start = None
        for line in output.splitlines():
            if "silence_start:" in line:
                current_start = float(line.split("silence_start:")[1].strip())
            elif "silence_end:" in line and current_start is not None:
                parts = line.split("silence_end:")[1].split('|')
                end_time = float(parts[0].strip())
                silence_durations.append(end_time - current_start)
                current_start = None
        total_silence = sum(silence_durations)

        duration = get_audio_duration(path)
        if duration <= 0:
            return 1.0  # Assume fully silent if duration unknown

        ratio = total_silence / duration
        return min(max(ratio, 0.0), 1.0)  # Clamp between 0 and 1
    except Exception as e:
        logger.warning(f"Failed to estimate silence ratio for {path}: {e}")
        return 1.0

def check_audio_quality(
    path: str,
    min_duration: float = 2.0,
    max_duration: float = 60 * 60 * 2,
    min_sample_rate: int = 16000,
    min_bitrate: int = 32000,
    min_rms_db: float = -40.0,
    max_silence_ratio: float = 0.6
) -> tuple[bool, str]:
    """
    Runs a set of audio quality checks using ffmpeg and returns (ok, reason).

    Args:
        path: Path to audio file.
        min_duration: Minimum allowed duration in seconds.
        max_duration: Maximum allowed duration in seconds.
        min_sample_rate: Minimum sample rate in Hz.
        min_bitrate: Minimum bitrate in bps.
        min_rms_db: Minimum average volume in dBFS.
        max_silence_ratio: Maximum allowed ratio of silence.

    Returns:
        Tuple[bool, str]: (True, "OK") if passes; (False, reason) otherwise.
    """
    if not os.path.isfile(path):
        return False, "File does not exist"

    if not is_supported_format(path):
        return False, "Unsupported audio format"

    duration = get_audio_duration(path)
    if duration < 0:
        return False, "Unable to determine audio duration"
    if duration < min_duration:
        return False, "Audio too short"
    if duration > max_duration:
        return False, "Audio too long"

    sample_rate, _channels = get_sample_rate_channels(path)
    if sample_rate < min_sample_rate:
        return False, f"Sample rate too low: {sample_rate} Hz"

    bitrate = get_bitrate(path)
    if bitrate < min_bitrate:
        return False, f"Bitrate too low: {bitrate} bps"

    rms_db = get_rms_volume(path)
    if rms_db is None or rms_db < min_rms_db:
        return False, f"Audio too quiet (mean volume {rms_db} dB)"

    silence_ratio = get_silence_ratio(path)
    if silence_ratio > max_silence_ratio:
        return False, f"Audio too silent ({silence_ratio*100:.1f}% silence)"

    return True, "OK"

def convert_to_wav(input_path: str, output_path: str) -> None:
    """
    Convert input audio file to mono 16kHz WAV using ffmpeg.

    Raises subprocess.CalledProcessError on failure.
    """
    logger.info(f"Converting {input_path} to WAV {output_path}")
    subprocess.run([
        "ffmpeg", "-y", "-i", input_path,
        "-ac", "1", "-ar", "16000", output_path
    ], check=True)

def trim_silence(input_path: str, output_path: str) -> bool:
    """
    Trim silence from beginning and end of audio using ffmpeg silenceremove filter.

    Returns True on success, False on failure.
    """
    logger.info(f"Trimming silence from {input_path}")
    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", input_path,
            "-af", ("silenceremove=start_periods=1:start_duration=0.5:start_threshold=-50dB:"
                    "stop_periods=1:stop_duration=0.5:stop_threshold=-50dB"),
            output_path
        ], check=True)
        return True
    except subprocess.CalledProcessError as e:
        logger.warning(f"Silence trimming failed: {e}")
        return False
