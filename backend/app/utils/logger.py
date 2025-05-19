"""
logger.py

Centralized logger configuration for the AI Meeting Summarizer project.

Created by Eric Morse
Date: 2024-05-18

- Configures a singleton logger for the application.
- Logs to a rotating file (`logs/server.log`) and to the console (for warnings/errors).
- File logs are rotated after 5MB, keeping up to 2 backups.
- Ensures that duplicate handlers are not added upon repeated imports.

Usage:
    from app.utils.logger import logger
    logger.info("message")
"""

import logging
from logging.handlers import RotatingFileHandler
import os

# Ensure logs directory exists (../logs relative to this file)
log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, 'server.log')

# Create a singleton logger
logger = logging.getLogger('MeetingSummarizer')
logger.setLevel(logging.INFO)

# Rotating file handler (5MB per file, 2 backups)
file_handler = RotatingFileHandler(
    log_file, maxBytes=5 * 1024 * 1024, backupCount=2, encoding="utf-8"
)
file_handler.setFormatter(
    logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
)

# Console handler for warnings and above
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)
console_handler.setFormatter(
    logging.Formatter('%(levelname)s: %(message)s')
)

# Attach handlers only once (prevents duplicate logs if re-imported)
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# Usage (for other modules):
#   from app.utils.logger import logger
#   logger.info("Info message")
#   logger.warning("Warning message")
#   logger.error("Error message")
