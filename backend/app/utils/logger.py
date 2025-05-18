import logging
from logging.handlers import RotatingFileHandler
import os

# Ensure logs directory exists
log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, 'server.log')

# Create logger (singleton)
logger = logging.getLogger('MeetingSummarizer')
logger.setLevel(logging.INFO)

# File handler with rotation
file_handler = RotatingFileHandler(
    log_file, maxBytes=5 * 1024 * 1024, backupCount=2, encoding="utf-8"
)
file_handler.setFormatter(
    logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
)

# Console handler for warnings/errors
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)
console_handler.setFormatter(
    logging.Formatter('%(levelname)s: %(message)s')
)

# Ensure handlers aren't duplicated if re-imported
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# For other modules: from app.utils.logger import logger
