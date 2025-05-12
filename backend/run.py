# Flask setup and required imports
from flask import Flask, request, jsonify  # Web app and request/response handling
from flask_cors import CORS  # For enabling cross-origin requests from frontend
import nltk  # Natural Language Toolkit for text processing
import os  # File system operations
import requests  # For making HTTP requests to AssemblyAI
import subprocess  # Running ffmpeg for audio processing
import datetime  # For timestamping transcript logs
import logging  # For app logging
import time  # For polling loop delays
from nltk.tokenize import sent_tokenize  # Sentence tokenizer for summarization
from dotenv import load_dotenv
load_dotenv()  # Load variables from .env

import os
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
if not ASSEMBLYAI_API_KEY:
    raise ValueError("Missing ASSEMBLYAI_API_KEY environment variable.")

# Download sentence tokenizer
nltk.download('punkt')

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024  # Limit uploads to 25MB

# Enable CORS for local React frontend
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"***REMOVED******REMOVED***)

# Configure logging to file with timestamps
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Load the API key from environment variable
#ASSEMBLYAI_API_KEY = os.environ.get("ASSEMBLYAI_API_KEY")
ASSEMBLYAI_API_KEY = '***REMOVED***'
if not ASSEMBLYAI_API_KEY:
    raise ValueError("Missing ASSEMBLYAI_API_KEY environment variable.")

# Helper function to log transcripts to timestamped files
def log_transcript_to_file(transcript):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs("transcripts", exist_ok=True)
    path = os.path.join("transcripts", f"transcript_{timestamp***REMOVED***.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(transcript)
    logging.info(f"Transcript logged to {path***REMOVED***")

# Endpoint for receiving and processing uploaded audio files
@app.route('/process-audio', methods=['POST'])
def process_audio():
    logging.info("Received audio upload request")

    # Grab uploaded audio file
    file = request.files.get('audio')
    if not file:
        logging.error("No file uploaded")
        return jsonify({"error": "No file uploaded"***REMOVED***), 400

    # Check file type (audio/wav, audio/mp3, etc.)
    if not file.content_type.startswith('audio/'):
        return jsonify({"error": "Invalid file type. Only audio files are allowed."***REMOVED***), 400

    # Check file size (max 25MB)
    if len(file.read()) > 25 * 1024 * 1024:
        return jsonify({"error": "File too large! Max 25MB allowed."***REMOVED***), 400
    file.seek(0)  # Reset file pointer after reading

    # Define file paths for original, converted, and trimmed audio
    original_path = "original_audio.wav"
    converted_path = "converted_audio.wav"
    trimmed_path = "trimmed_audio.wav"
    file.save(original_path)
    logging.info(f"Saved file: {original_path***REMOVED***")

    try:
        # Convert audio to mono, 16kHz WAV using ffmpeg
        subprocess.run([
            "ffmpeg", "-y",
            "-i", original_path,
            "-ac", "1",
            "-ar", "16000",
            converted_path
        ], check=True)
        logging.info(f"Converted audio saved as: {converted_path***REMOVED***")
    except subprocess.CalledProcessError as e:
        logging.exception("FFmpeg conversion failed")
        return jsonify({"error": "Audio conversion failed", "details": str(e)***REMOVED***), 500

    # Check for silence in the converted audio
    try:
        silence_check = subprocess.run(
            ["ffmpeg", "-i", converted_path, "-af", "silencedetect=noise=-30dB:d=1", "-f", "null", "-"],
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        if "silencedetect" not in silence_check.stderr:
            logging.warning("Likely silent or unreadable audio.")
    except subprocess.CalledProcessError as e:
        if "silence_start" in e.stderr and "silence_end" in e.stderr:
            logging.info("Silence detected but audio content exists.")
        else:
            logging.error("Audio appears completely silent.")
            return jsonify({"error": "Audio file appears to contain only silence."***REMOVED***), 400

    # Try trimming leading and trailing silence
    try:
        subprocess.run([
            "ffmpeg", "-y",
            "-i", converted_path,
            "-af", "silenceremove=start_periods=1:start_duration=0.5:start_threshold=-50dB:stop_periods=1:stop_duration=0.5:stop_threshold=-50dB",
            trimmed_path
        ], check=True)
        logging.info("Silence trimmed from audio.")
        final_path = trimmed_path
    except subprocess.CalledProcessError:
        logging.warning("Silence trimming failed; using untrimmed audio.")
        final_path = converted_path

    if not os.path.exists(final_path) or os.stat(final_path).st_size == 0:
        logging.error("Final audio file is empty or missing.")
        return jsonify({"error": "Final audio file is empty or missing"***REMOVED***), 400

    try:
        with open(final_path, 'rb') as f:
            upload_res = requests.post(
                'https://api.assemblyai.com/v2/upload',
                headers={'authorization': ASSEMBLYAI_API_KEY***REMOVED***,
                data=f
            )
        upload_url = upload_res.json()['upload_url']
        logging.info(f"Audio uploaded to AssemblyAI: {upload_url***REMOVED***")

        transcript_res = requests.post(
            'https://api.assemblyai.com/v2/transcript',
            headers={'authorization': ASSEMBLYAI_API_KEY, 'content-type': 'application/json'***REMOVED***,
            json={'audio_url': upload_url, 'punctuate': True***REMOVED***
        )
        transcript_id = transcript_res.json()['id']
        logging.info(f"Transcription requested, ID: {transcript_id***REMOVED***")

        polling_url = f'https://api.assemblyai.com/v2/transcript/{transcript_id***REMOVED***'
        while True:
            status_res = requests.get(polling_url, headers={'authorization': ASSEMBLYAI_API_KEY***REMOVED***)
            status_data = status_res.json()

            if status_data['status'] == 'completed':
                transcript = status_data['text']
                log_transcript_to_file(transcript)
                return jsonify({'transcript': transcript***REMOVED***)
            elif status_data['status'] == 'error':
                logging.error(f"AssemblyAI Error: {status_data.get('error')***REMOVED***")
                return jsonify({"error": "AssemblyAI transcription failed", "details": status_data.get("error")***REMOVED***), 500

            time.sleep(3)

    except Exception as e:
        logging.exception("Failed during transcription process")
        return jsonify({"error": "Transcription failed", "details": str(e)***REMOVED***), 500
    finally:
        for path in [original_path, converted_path, trimmed_path]:
            if os.path.exists(path):
                os.remove(path)

@app.route('/process-json', methods=['POST'])
def process_json():
    data = request.get_json()
    transcript = data.get("transcript")

    if not transcript or (isinstance(transcript, str) and not transcript.strip()):
        logging.error("No transcript found in the request data.")
        return jsonify({"error": "Transcript is empty or missing."***REMOVED***), 400

    full_text = transcript if isinstance(transcript, str) else " ".join(
        [segment.get("text", "") for segment in transcript]
    )

    logging.info(f"Full transcript received: {full_text[:100]***REMOVED***...")

    prompt = f"""
    You are an assistant summarizing meeting transcripts.

    Transcript:
    {full_text***REMOVED***

    Extract the following:
    1. Summary (bullet points)
    2. Action Items (with responsible people if mentioned)
    3. Decisions made

    Respond in JSON format like:
    {{
      "summary": [...],
      "actions": [...],
      "decisions": [...]
    ***REMOVED******REMOVED***
    """

    sentences = sent_tokenize(full_text)
    summary = []
    actions = []
    decisions = []

    action_keywords = [
        "will", "must", "should", "needs to", "is responsible for",
        "will handle", "is tasked with", "take the lead in"
    ]

    for sentence in sentences:
        lower = sentence.lower()
        if "decided" in lower or "decision" in lower or "agree" in lower:
            decisions.append(sentence)
        elif any(k in lower for k in action_keywords):
            actions.append(sentence)
        else:
            summary.append(sentence)

    logging.info(f"Extracted summary: {summary***REMOVED***")
    logging.info(f"Extracted actions: {actions***REMOVED***")
    logging.info(f"Extracted decisions: {decisions***REMOVED***")

    return jsonify({
        "summary": summary,
        "actions": actions,
        "decisions": decisions
    ***REMOVED***)


if __name__ == '__main__':
    app.run(debug=True)
