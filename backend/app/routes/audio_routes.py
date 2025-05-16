from flask import Blueprint, request, jsonify
from datetime import datetime
import os
import time
import requests
from app.utils.logger import logger
from app.utils.logging_utils import log_transcript_to_file
from app.services.audio_processor import convert_to_wav, trim_silence
from pathlib import Path
import json

audio_bp = Blueprint('audio', __name__)

# Load secrets
SECRETS_PATH = Path.home() / ".app_secrets" / "env.json"
with open(SECRETS_PATH) as f:
    secrets = json.load(f)

ASSEMBLYAI_API_KEY = secrets.get("ASSEMBLYAI_API_KEY")
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@audio_bp.route('/process-audio', methods=['POST'])
def process_audio():
    original_path = converted_path = trimmed_path = None
    try:
        file = request.files.get('audio')
        if not file or not file.content_type.startswith('audio/'):
            return jsonify({"error": "Invalid file or missing."}), 400

        file.seek(0, os.SEEK_END)
        if file.tell() > 25 * 1024 * 1024:
            return jsonify({"error": "File too large! Max 25MB allowed."}), 400
        file.seek(0)

        original_path = "original_audio.wav"
        converted_path = "converted_audio.wav"
        trimmed_path = "trimmed_audio.wav"
        file.save(original_path)

        # Audio processing
        convert_to_wav(original_path, converted_path)
        trim_success = trim_silence(converted_path, trimmed_path)
        final_path = trimmed_path if trim_success else converted_path

        # Upload to AssemblyAI
        with open(final_path, 'rb') as f:
            upload_res = requests.post(
                'https://api.assemblyai.com/v2/upload',
                headers={'authorization': ASSEMBLYAI_API_KEY},
                data=f
            )
        logger.info("Upload response: %s", upload_res.text)
        upload_url = upload_res.json()['upload_url']

        # Transcription
        transcript_res = requests.post(
            'https://api.assemblyai.com/v2/transcript',
            headers={
                'authorization': ASSEMBLYAI_API_KEY,
                'content-type': 'application/json'
            },
            json={
                'audio_url': upload_url,
                'punctuate': True,
                'entity_detection': True
            }
        )
        transcript_id = transcript_res.json()['id']
        polling_url = f'https://api.assemblyai.com/v2/transcript/{transcript_id}'

        while True:
            status_res = requests.get(polling_url, headers={'authorization': ASSEMBLYAI_API_KEY})
            status_data = status_res.json()
            if status_data['status'] == 'completed':
                transcript = status_data['text']
                entities = status_data.get('entities', [])

                log_transcript_to_file(transcript)
                logger.info("Transcription completed.")
                return jsonify({'transcript': transcript, 'entities': entities})

            elif status_data['status'] == 'error':
                return jsonify({"error": "Transcription failed", "details": status_data.get("error")}), 500

            time.sleep(3)

    except Exception as e:
        logger.exception("Unhandled error in /process-audio")
        return jsonify({"error": "Unexpected server error", "details": str(e)}), 500

    finally:
        for path in filter(None, [original_path, converted_path, trimmed_path]):
            if os.path.exists(path):
                os.remove(path)

