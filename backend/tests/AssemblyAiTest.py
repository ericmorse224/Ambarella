import requests
import time

ASSEMBLYAI_API_KEY = ***REMOVED***

def upload_audio(file_path):
    headers = {'authorization': ASSEMBLYAI_API_KEY***REMOVED***
    with open(file_path, 'rb') as f:
        response = requests.post(
            'https://api.assemblyai.com/v2/upload',
            headers=headers,
            data=f
        )
    response.raise_for_status()
    return response.json()['upload_url']

def start_transcription(audio_url):
    endpoint = 'https://api.assemblyai.com/v2/transcript'
    json_data = {'audio_url': audio_url, 'punctuate': True, 'language_code': 'en_us'***REMOVED***
    headers = {
        'authorization': ASSEMBLYAI_API_KEY,
        'content-type': 'application/json'
    ***REMOVED***
    response = requests.post(endpoint, json=json_data, headers=headers)
    response.raise_for_status()
    return response.json()['id']

def wait_for_completion(transcript_id):
    endpoint = f'https://api.assemblyai.com/v2/transcript/{transcript_id***REMOVED***'
    headers = {'authorization': ASSEMBLYAI_API_KEY***REMOVED***
    while True:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        status = response.json()['status']
        if status == 'completed':
            return response.json()['text']
        elif status == 'error':
            raise Exception(f"Transcription failed: {response.json()['error']***REMOVED***")
        time.sleep(3)

def transcribe(file_path):
    print("Uploading audio...")
    audio_url = upload_audio(file_path)
    print("Starting transcription...")
    transcript_id = start_transcription(audio_url)
    print("Waiting for transcription to complete...")
    text = wait_for_completion(transcript_id)
    print("Transcription complete:\n")
    print(text)

# Run it
transcribe("Recording.wav")
