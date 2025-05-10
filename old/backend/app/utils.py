### backend/app/utils.py
import json

def load_meeting_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)
