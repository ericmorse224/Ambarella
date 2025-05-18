from flask import Blueprint, request, jsonify
import os
from datetime import datetime, timezone, timedelta
import time
from app.utils.logger import logger
from app.utils.logging_utils import log_transcript_to_file, log_event
from app.services.audio_processor import check_audio_quality, convert_to_wav, trim_silence, get_audio_duration, get_sample_rate_channels, get_bitrate
import whisper

whisper_model = whisper.load_model("base")
audio_bp = Blueprint('audio', __name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_client_ip():
    # Optionally use request headers for X-Forwarded-For in production/reverse proxy
    return request.headers.get('X-Forwarded-For', request.remote_addr)

@audio_bp.route('/process-audio', methods=['POST'])
def process_audio():
    """
    Accepts audio upload, checks quality, logs detailed analytics/events, and returns transcript.
    """
    original_path = converted_path = trimmed_path = None
    upload_start = time.time()
    try:
        file = request.files.get('audio')
        if not file or not file.content_type.startswith('audio/'):
            return jsonify({"error": "Invalid file or missing."}), 400

        file.seek(0, os.SEEK_END)
        reported_size = file.tell()
        if reported_size > 25 * 1024 * 1024:
            return jsonify({"error": "File too large! Max 25MB allowed."}), 400
        file.seek(0)

        original_path = "original_audio.wav"
        converted_path = "converted_audio.wav"
        trimmed_path = "trimmed_audio.wav"
        file.save(original_path)

        # --- Audio quality check and metadata ---
        ok, reason = check_audio_quality(original_path)
        duration = get_audio_duration(original_path)
        sample_rate, channels = get_sample_rate_channels(original_path)
        bitrate = get_bitrate(original_path)
        file_meta = {
            "filename": getattr(file, "filename", None),
            "content_type": getattr(file, "content_type", None),
            "reported_size": reported_size,
            "duration": duration,
            "sample_rate": sample_rate,
            "channels": channels,
            "bitrate": bitrate
        }
        client_ip = get_client_ip()
        timestamp = datetime.now(timezone.utc).isoformat()

        if not ok:
            logger.warning(f"Audio rejected: {reason}")
            # Log the failed upload as an event (with all metadata)
            log_event({
                "type": "audio_quality_failed",
                "timestamp": timestamp,
                "user_agent": request.headers.get("User-Agent"),
                "ip": client_ip,
                **file_meta,
                "reason": reason,
                "outcome": "failure"
            })
            return jsonify({"error": reason, "quality_warning": reason}), 400

        # Convert and trim
        convert_to_wav(original_path, converted_path)
        trim_success = trim_silence(converted_path, trimmed_path)
        final_path = trimmed_path if trim_success else converted_path

        # Whisper transcription
        transcribe_start = time.time()
        result = whisper_model.transcribe(final_path)
        transcript = result["text"]
        transcribe_time = time.time() - transcribe_start
        transcript_length = len(transcript.split())

        log_transcript_to_file(transcript)
        logger.info("Transcription completed.")

        # Log the successful upload with analytics
        log_event({
            "type": "audio_upload_success",
            "timestamp": timestamp,
            "user_agent": request.headers.get("User-Agent"),
            "ip": client_ip,
            **file_meta,
            "outcome": "success",
            "transcript_length": transcript_length,
            "transcribe_time_sec": round(transcribe_time, 2),
            "processing_time_sec": round(time.time() - upload_start, 2)
        })

        return jsonify({'transcript': transcript, 'entities': []})

    except Exception as e:
        logger.exception("Unhandled error in /process-audio")
        log_event({
            "type": "audio_route_exception",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "user_agent": request.headers.get("User-Agent"),
            "ip": get_client_ip(),
            "error": str(e),
            "outcome": "exception"
        })
        return jsonify({"error": "Unexpected server error", "details": str(e)}), 500

    finally:
        # Always clean up temp audio files
        for path in filter(None, [original_path, converted_path, trimmed_path]):
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except Exception as cleanup_err:
                    logger.warning(f"Failed to delete temp file {path}: {cleanup_err}")
