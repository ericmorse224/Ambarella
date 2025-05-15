def generate_event_data_from_action(action_text):
    # Dummy time window for simplicity
    from datetime import datetime, timedelta
    now = datetime.utcnow()
    start_time = now + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)

    return {
        "title": action_text[:60],
        "description": "Auto-created from meeting action item.",
        "start_time": start_time.isoformat() + "Z",
        "end_time": end_time.isoformat() + "Z",
    }

