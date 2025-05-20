from app.services.nlp_analysis import extract_actions_nltk

transcript = "Also premiered on the meeting slides, Bob needs to book the conference, Carol will send out the calendar invites. Dave should print the agenda, Aaron is assigned to take notes, Frank must order lunch for a team."
actions = extract_actions_nltk(transcript)
print(actions)
