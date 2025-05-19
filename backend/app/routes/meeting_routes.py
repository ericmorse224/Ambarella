"""
meeting_routes.py

Flask Blueprint for meeting-related dashboard routes in the
AI Meeting Summarizer project.

Created by Eric Morse
Date: 2024-05-18

Features:
- API endpoint to retrieve all 'meeting_meta' event log entries.
- Graceful handling of missing directories, parse errors, and file errors.
- Logs parsing errors and file read issues as structured events for auditing.

Dependencies: Flask, os, json, app.utils.logging_utils
"""

from flask import Blueprint, jsonify
import os
import json
from app.utils.logging_utils import log_event

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route("/api/meetings/meta", methods=["GET"])
def get_meeting_meta_logs():
    """
    Returns all 'meeting_meta' event log entries as a JSON array, sorted newest first.

    - Handles missing log directory by returning empty logs.
    - Handles malformed log lines by counting them, skipping, and logging as error events.
    - Handles file read errors by skipping files and logging as file-level error events.
    - For each error, logs a structured error event in the log.

    Returns:
        JSON object:
        {
            "logs": [ ... ],              # list of meeting_meta event log dicts
            "skipped_lines": int,         # number of lines skipped due to parse errors
            "skipped_files": [ ... ]      # list of files that could not be parsed or opened
        }
    """
    logs = []
    directory = "event_logs"
    skipped_lines = 0
    skipped_files = set()
    if not os.path.isdir(directory):
        return jsonify({"logs": [], "skipped_lines": 0, "skipped_files": []})

    for filename in os.listdir(directory):
        if filename.startswith("event_log_") and filename.endswith(".jsonl"):
            path = os.path.join(directory, filename)
            try:
                with open(path, encoding="utf-8") as f:
                    for i, line in enumerate(f, 1):
                        try:
                            entry = json.loads(line)
                            if entry.get("type") == "meeting_meta":
                                logs.append(entry)
                        except Exception as e:
                            skipped_lines += 1
                            skipped_files.add(filename)
                            # Log the error event for this line
                            log_event({
                                "type": "log_parse_error",
                                "file": filename,
                                "line_number": i,
                                "error": str(e),
                                "raw_line": line.strip()
                            })
                            continue
            except Exception as e:
                # If the file can't be opened, log a file-level error event
                skipped_files.add(filename)
                log_event({
                    "type": "log_file_error",
                    "file": filename,
                    "error": str(e)
                })
                continue

    logs.sort(key=lambda x: x.get("logged_at", ""), reverse=True)
    return jsonify({
        "logs": logs,
        "skipped_lines": skipped_lines,
        "skipped_files": sorted(list(skipped_files))
    })
