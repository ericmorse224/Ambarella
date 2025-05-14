import openai
import logging
import os
from dotenv import load_dotenv
from datetime import datetime

dotenv_path = os.path.expanduser('~/.app_secrets/.env')
load_dotenv(dotenv_path=dotenv_path)

openai.api_key = os.getenv("OPENAI_API_KEY")

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
    
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt***REMOVED***],
        max_tokens=600,
        temperature=0.2
    )

    logging.info(f"LLM PROMPT:\n{prompt***REMOVED***")

    output = pipe(prompt, max_new_tokens=512)[0]["generated_text"]
    logging.info("RAW LLM OUTPUT:\n" + output)
    return output
