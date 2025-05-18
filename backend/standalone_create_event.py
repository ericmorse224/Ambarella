from app.services.calendar_integration import create_calendar_event
from datetime import datetime, timedelta, timezone

title = "Follow-up: Frank"
description = "Test description\n\nOwner: Frank"
start_time = datetime.now(timezone.utc) + timedelta(hours=1)
end_time = start_time + timedelta(minutes=30)
response = create_calendar_event(title, description, start_time.isoformat(), end_time.isoformat())
print(response)
