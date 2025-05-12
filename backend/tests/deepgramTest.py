# Import the requests library to send HTTP requests
import requests

# Load the API key from environment variable
DG_API_KEY = os.environ.get("DEEPGRAM_API_KEY")

if not DG_API_KEY:
    raise ValueError("Missing DEEPGRAM_API_KEY environment variable.")

# Debugging output to confirm the API key format (never print API keys in production!)
print(f"Sending Deepgram API Key: Token {DG_API_KEY***REMOVED***")

# Open the audio file in binary read mode
with open("Recording.wav", "rb") as f:
    # Send a POST request to Deepgram's transcription API endpoint
    res = requests.post(
        "https://api.deepgram.com/v1/listen",  # Endpoint for real-time transcription
        headers={
            "Authorization": f"Token {DG_API_KEY***REMOVED***"  # Authentication header using your API token
        ***REMOVED***,
        files={
            "file": f  # Attach the opened audio file to the request payload
        ***REMOVED***,
    )

    # Print the HTTP status code returned by the server (e.g., 200 = success)
    print(f"Status Code: {res.status_code***REMOVED***")

    # Print the full response body (likely JSON containing the transcript or error)
    print(f"Response: {res.text***REMOVED***")
