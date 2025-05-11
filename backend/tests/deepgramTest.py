import requests

DG_API_KEY = ***REMOVED***
print(f"Sending Deepgram API Key: Token {DG_API_KEY***REMOVED***")

# Open the audio file for reading
with open("Recording.wav", "rb") as f:
    res = requests.post(
        "https://api.deepgram.com/v1/listen",  # Deepgram API URL
        headers={"Authorization": f"Token {DG_API_KEY***REMOVED***"***REMOVED***,  # Correct header format (Token)
        files={"file": f***REMOVED***,  # Attach the audio file
    )

    # Output the response for debugging
    print(f"Status Code: {res.status_code***REMOVED***")
    print(f"Response: {res.text***REMOVED***")
