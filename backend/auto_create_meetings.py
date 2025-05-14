from zoho_meeting_utils import refresh_access_token
import requests
import logging

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
            "topic": f"Action Item {i+1***REMOVED***",
            "agenda": action,
            "meetingType": "WEBINAR",
            "startTime": "2025-05-15T10:00:00",  # Ideally use actual time parsing/NLP
            "duration": 30,
            "timezone": "America/New_York"
        ***REMOVED***

        try:
            response = requests.post(
                "https://meeting.zoho.com/api/v1/meetings",
                headers={"Authorization": f"Zoho-oauthtoken {access_token***REMOVED***"***REMOVED***,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            created.append(result)
            logging.info(f"✅ Created meeting for action: {action***REMOVED***")

        except Exception as e:
            logging.error(f"❌ Failed to create meeting for action '{action***REMOVED***': {e***REMOVED***")

    return created
