"""
standalone_create_event.py

Author: Eric Morse
Date: May 11th, 2025

Description:
-------------
A standalone script to demonstrate and test the creation of a calendar event
using the application's calendar integration service. This script sets up
example event data and invokes the `create_calendar_event` function, then
prints the response.

Usage:
-------
Run this script independently to create a test calendar event.

Requirements:
-------------
- The application backend (with `calendar_integration.py`) must be available.
- Ensure all necessary dependencies are installed and environment is set up.
"""

from app.services.calendar_integration import create_calendar_event
from datetime import datetime, timedelta, timezone

# Set up example event details.
title = "Follow-up: Frank"  # Title of the event
description = "Test description\n\nOwner: Frank"  # Event description (can include owner or additional context)

# Schedule event to start 1 hour from now (in UTC)
start_time = datetime.now(timezone.utc) + timedelta(hours=1)

# Set the event to last 30 minutes
end_time = start_time + timedelta(minutes=30)

# Create the calendar event using the integration function.
# The function expects ISO-formatted datetime strings.
response = create_calendar_event(
    title,
    description,
    start_time.isoformat(),
    end_time.isoformat()
)

# Output the response to the terminal for inspection.
print(response)
