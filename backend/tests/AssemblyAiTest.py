import requests  # Used for making HTTP requests to the AssemblyAI API
import time      # Used for adding delay while polling the transcription status
import os        # Required to load environment variables

# Load the AssemblyAI API key securely from environment variables
ASSEMBLYAI_API_KEY = os.environ.get("ASSEMBLYAI_API_KEY")

# Check if the API key was loaded; if not, raise an error to prevent unauthorized requests
if not ASSEMBLYAI_API_KEY:
    raise ValueError("Missing ASSEMBLYAI_API_KEY environment variable.")

def upload_audio(file_path):
    """
    Uploads an audio file to AssemblyAI's server for transcription.

    Parameters:
        file_path (str): The path to the local audio file.

    Returns:
        str: A URL pointing to the uploaded audio file.
    """
    headers = {'authorization': ASSEMBLYAI_API_KEY***REMOVED***

    # Open the audio file in binary mode and send it to the upload endpoint
    with open(file_path, 'rb') as f:
        response = requests.post(
            'https://api.assemblyai.com/v2/upload',
            headers=headers,
            data=f
        )

    # Raise an error if the request was not successful
    response.raise_for_status()

    # Return the URL of the uploaded file
    return response.json()['upload_url']

def start_transcription(audio_url):
    """
    Starts a transcription job using a previously uploaded audio file.

    Parameters:
        audio_url (str): The URL to the uploaded audio file.

    Returns:
        str: The ID of the transcription job.
    """
    endpoint = 'https://api.assemblyai.com/v2/transcript'
    json_data = {
        'audio_url': audio_url,
        'punctuate': True,         # Request punctuation in the transcript
        'language_code': 'en_us'   # Specify the language of the audio
    ***REMOVED***
    headers = {
        'authorization': ASSEMBLYAI_API_KEY,
        'content-type': 'application/json'
    ***REMOVED***

    # Send the transcription request
    response = requests.post(endpoint, json=json_data, headers=headers)

    # Raise an error if the request was not successful
    response.raise_for_status()

    # Return the transcription ID
    return response.json()['id']

def wait_for_completion(transcript_id):
    """
    Polls the AssemblyAI API until the transcription job is complete.

    Parameters:
        transcript_id (str): The ID of the transcription job.

    Returns:
        str: The completed transcript text.
    """
    endpoint = f'https://api.assemblyai.com/v2/transcript/{transcript_id***REMOVED***'
    headers = {'authorization': ASSEMBLYAI_API_KEY***REMOVED***

    while True:
        # Get the current status of the transcription job
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()

        status = response.json()['status']

        # Check if the job is complete
        if status == 'completed':
            return response.json()['text']
        elif status == 'error':
            # Raise an exception with the error message
            raise Exception(f"Transcription failed: {response.json()['error']***REMOVED***")

        # Wait 3 seconds before polling again to avoid rate-limiting
        time.sleep(3)

def transcribe(file_path):
    """
    Handles the complete process of uploading, transcribing, and retrieving the transcript.

    Parameters:
        file_path (str): Path to the audio file to be transcribed.
    """
    print("Uploading audio...")
    audio_url = upload_audio(file_path)

    print("Starting transcription...")
    transcript_id = start_transcription(audio_url)

    print("Waiting for transcription to complete...")
    text = wait_for_completion(transcript_id)

    print("Transcription complete:\n")
    print(text)

# Execute the transcription pipeline for a file called "Recording.wav"
transcribe("Recording.wav")
