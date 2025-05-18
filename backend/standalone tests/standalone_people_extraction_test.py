from app.utils.entity_utils import extract_entities, extract_people_from_entities
# standalone test that details the process to acquire people from a transcript.
transcript = "Alice will prepare the report. Bob will schedule the meeting."

entities = extract_entities(transcript)
people = extract_people_from_entities(entities)

print("Extracted people:", people)
