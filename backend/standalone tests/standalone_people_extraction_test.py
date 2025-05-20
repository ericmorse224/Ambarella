"""
standalone_people_extraction_test.py

Author: Eric Morse  
Date: May 11th, 2025

Description:
    This standalone script demonstrates how to extract people entities from a given meeting transcript.
    It uses utility functions from the `app.utils.entity_utils` module: `extract_entities` to identify
    entities in the transcript and `extract_people_from_entities` to extract people names from the identified entities.

Usage:
    Run this script directly to print the list of extracted people from the sample transcript.

Dependencies:
    - app.utils.entity_utils: The script assumes this module exists and provides
      the required entity extraction functions.

Example Output:
    Extracted people: ['Alice', 'Bob']
"""

from app.utils.entity_utils import extract_entities, extract_people_from_entities

# Sample meeting transcript to extract people from
transcript = "Alice will prepare the report. Bob will schedule the meeting."

# Step 1: Extract entities from the transcript
entities = extract_entities(transcript)

# Step 2: Extract people names from the list of entities
people = extract_people_from_entities(entities)

# Output the result
print("Extracted people:", people)
