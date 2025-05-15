import requests
import json

#https://accounts.zoho.com/oauth/v2/auth?scope=ZohoMeeting.meeting.ALL&client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=http://localhost:5000/zoho/callback&access_type=offline&prompt=consent
#You must have code_capture.py running when accessing above weblink.
#Input your Client_ID and Client_Secret below. (Obtained from https://api-console.zoho.com/)

CLIENT_ID = "1000.8Z185SGDR9RIJ9EUJR0S49GEAZBIQK"
CLIENT_SECRET = "0b1af65a055e5932641d3cadf3ddfd9a359d14ef1f"
REDIRECT_URI = "http://localhost:5000/zoho/callback"
AUTH_CODE = "1000.518920d268ed62feac58cacabcc5fcd2.e9d1495b289e564e21ccc7cfbc2c6865"  # ← Replace this!

token_url = "https://accounts.zoho.com/oauth/v2/token"

params = {
    "grant_type": "authorization_code",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": REDIRECT_URI,
    "code": AUTH_CODE
}

response = requests.post(token_url, params=params)

if response.status_code == 200:
    tokens = response.json()
    print("✅ Access token obtained:")
    print(json.dumps(tokens, indent=2))

    # Save to file
    with open("zoho_tokens.json", "w") as f:
        json.dump(tokens, f, indent=2)
    print("✅ Tokens saved to zoho_tokens.json")

else:
    print("❌ Error:", response.status_code)
    print(response.text)

