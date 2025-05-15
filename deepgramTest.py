import requests

DG_API_KEY = ***REMOVED***

with open("Test1.m4a", "rb") as f:
    res = requests.post(
        "https://api.deepgram.com/v1/listen",
        headers={"Authorization": f"Bearer {DG_API_KEY}"},
        files={"file": f},
        params={"punctuate": "true", "language": "en"}
    )
    print(res.status_code)
    print(res.text)

