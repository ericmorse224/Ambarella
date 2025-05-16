from app.utils.zoho_utils import refresh_access_token, create_meeting
import requests
import logging
from datetime import datetime
from app.utils.logger import logger

# Auto-create meetings from extracted action items

def create_meetings_from_actions(actions: list):
    """
    Given a list of action item strings, attempt to create Zoho Meetings.
    """
    if not actions:
        logging.info("No action items to create meetings for.")
        return []

    access_token = refresh_access_token()
    created = []

    for i, action in enumerate(actions):
        # Create a default payload using the action string
        payload = {
            "topic": f"Action Item {i+1}",
            "agenda": action,
            "meetingType": "WEBINAR",
            "startTime": "2025-05-15T10:00:00",  # Ideally use actual time parsing/NLP
            "duration": 30,
            "timezone": "America/New_York"
        }

        try:
            response = requests.post(
                "https://meeting.zoho.com/api/v1/meetings",
                headers={"Authorization": f"Zoho-oauthtoken {access_token}"},
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            created.append(result)
            logging.info(f"✅ Created meeting for action: {action}")

        except Exception as e:
            logging.error(f"❌ Failed to create meeting for action '{action}': {e}")

    return created


def create_meeting(title, agenda, start_time):
    endpoint = "/meeting/v1/meetings"
    payload = {
        "topic": title,
        "agenda": agenda,
        "start_time": start_time,
        "duration": 30,
        "timezone": "America/New_York"
    }

    response = make_authorized_request(endpoint, method="POST", payload=payload)
    if response.ok:
        logging.info("✅ Zoho Meeting created.")
        return response.json()
    else:
        logging.error(f"❌ Failed to create meeting: {response.text}")
        return None

def update_meeting(meeting_key, access_token, payload):
    url = f"{API_BASE_URL}/meeting/v1/meetings/{meeting_key}"
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.put(url, headers=headers, json=payload)
    if not response.ok:
        raise Exception(f"Failed to update meeting: {response.text}")
    return response.json()

def auto_schedule_meetings(actions):
    results = []
    for action in actions:
        if not isinstance(action, dict):
            logger.warning("Skipping invalid action: %s", action)
            continue

        owner = action.get("owner", "None")
        agenda = action.get("text", "No details provided")
        title = f"Meeting: {owner}"
        start_time = datetime.now().isoformat()

        try:
            result = create_meeting(title, agenda, start_time)
            results.append(result)
        except Exception as e:
            logger.error("Failed to schedule meeting: %s", e)
            return []


    return results