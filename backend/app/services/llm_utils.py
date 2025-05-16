import os
import json
import logging
from pathlib import Path
from datetime import datetime
from openai import OpenAI
import re

# Load OpenAI API key
secrets = json.loads(Path.home().joinpath(".app_secrets", "env.json").read_text())
client = OpenAI(api_key=secrets["OPENAI_API_KEY"])

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
\"\"\"{cleaned_transcript}\"\"\"
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an intelligent assistant. Analyze the following meeting transcript and extract three things:\n\n1. A concise summary of the main topics.\n2. A list of action items, with clear assignments (e.g., \"Bob needs to...\").\n3. Any decisions made.\n\nOutput format:\nSummary:\n- ...\n\nAction Items:\n- [Person] needs to [task]\n\nDecisions:\n- ...",
            },
            {
                "role": "user",
                "content": transcript
            }
        ],
        temperature=0.2
    )

    output = response.choices[0].message.content
    logging.info(f"LLM Response:\n{output}")
    return output

import re

def parse_llm_sections(llm_output):
    if not llm_output:
        return {"summary": "", "actions": [], "decisions": []}

    # Extract sections with regex
    summary_match = re.search(r"Summary:\s*(.*?)(?=\nActions:|\nDecisions:|$)", llm_output, re.DOTALL)
    actions_match = re.search(r"Actions:\s*(.*?)(?=\nDecisions:|$)", llm_output, re.DOTALL)
    decisions_match = re.search(r"Decisions:\s*(.*)", llm_output, re.DOTALL)

    summary = summary_match.group(1).strip() if summary_match else ""
    raw_actions = actions_match.group(1).strip() if actions_match else ""
    raw_decisions = decisions_match.group(1).strip() if decisions_match else ""

    # Parse actions
    actions = []
    for line in raw_actions.splitlines():
        line = line.strip("-• ").strip()
        if not line:
            continue
        # Match "Name: Task"
        match = re.match(r"(\w+):\s*(.*)", line)
        if match:
            owner, task = match.groups()
            actions.append({"owner": owner.strip(), "text": task.strip()})
        else:
            actions.append({"text": line})

    # Parse decisions
    decisions = [line.strip("-• ").strip() for line in raw_decisions.splitlines() if line.strip()]

    return {
        "summary": summary,
        "actions": actions,
        "decisions": decisions
    }

#def parse_llm_sections(text):
#    def extract_section(name):
#        pattern = rf"{name}:\s*([\s\S]*?)(?=\n[A-Z][a-z]+:|\Z)"
#        match = re.search(pattern, text)
#        if match:
#            lines = match.group(1).strip().split('\n')
#            return [line.strip('-\u2022 ').strip() for line in lines if line.strip()]
#        return []
#
#    return {
#        "summary": extract_section("Summary"),
#        "actions": extract_section("Action Items"),
#        "decisions": extract_section("Decisions"),
#    }
