from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Set your API Key here
api_key = "YOUR_API_KEY"
url = "YOUR_API_URL"

authenticator = IAMAuthenticator(api_key)
speech_to_text = SpeechToTextV1(authenticator=authenticator)
speech_to_text.set_service_url(url)

def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        response = speech_to_text.recognize(
            audio=audio_file,
            content_type="audio/wav",
            model="en-US_BroadbandModel"
        ).get_result()
        print(response)

transcribe_audio("Recording.wav")

