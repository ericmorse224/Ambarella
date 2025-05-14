from openai import OpenAI
import logging
import os
from dotenv import load_dotenv
from datetime import datetime
import json
from pathlib import Path

secrets = json.loads(Path.home().joinpath(".app_secrets", "env.json").read_text())
client = OpenAI(api_key=secrets["OPENAI_API_KEY"])

def log_transcript_to_file(transcript):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs("transcripts", exist_ok=True)
    path = os.path.join("transcripts", f"transcript_{timestamp***REMOVED***.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(transcript)
    logging.info(f"Transcript logged to {path***REMOVED***")

def clean_transcript(transcript):
    lines = transcript.strip().split("\n")
    valid_lines = [line.strip() for line in lines if len(line.strip().split()) > 2]
    cleaned_transcript = " ".join(valid_lines)
    return cleaned_transcript

def generate_summary_and_extraction(transcript):
    logging.info("Generating LLM prompt...")
    cleaned_transcript = clean_transcript(transcript)

    prompt = f"""
You are an assistant specialized in summarizing and extracting structured information from meeting transcripts.

Extract clearly:

1. Summary (main points as clear, concise bullet points).
2. Action Items (clearly stated with responsible person if named; otherwise use "Someone").
3. Decisions (clearly stated; explicitly say "No decisions were made" if applicable).

Format exactly like this:

Summary:
- ...

Action Items:
- [Person/Someone] needs to ...

Decisions:
- ...

Transcript:
\"\"\"{cleaned_transcript***REMOVED***\"\"\"
"""
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an intelligent assistant. Analyze the following meeting transcript and extract three things:\n\n1. A concise summary of the main topics.\n2. A list of action items, with clear assignments (e.g., \"Bob needs to...\").\n3. Any decisions made.\n\nOutput format:\nSummary:\n- ...\n\nAction Items:\n- [Person] needs to [task]\n\nDecisions:\n- ...",
            ***REMOVED***,
            {
                "role": "user",
                "content": transcript
            ***REMOVED***
        ],
        temperature=0.2
    )
    output = response.choices[0].message.content


    logging.info(f"LLM PROMPT:\n{prompt***REMOVED***")

    output = pipe(prompt, max_new_tokens=512)[0]["generated_text"]
    logging.info("RAW LLM OUTPUT:\n" + output)
    return output
