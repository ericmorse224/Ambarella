### backend/app/extraction.py
def extract_actions(transcript):
    return [
        entry for entry in transcript
        if "will" in entry["text"] or "need to" in entry["text"]
    ]

def extract_decisions(transcript):
    return [
        entry for entry in transcript
        if "decided" in entry["text"] or "agreement" in entry["text"]
    ]
