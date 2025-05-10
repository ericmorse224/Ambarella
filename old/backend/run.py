from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
CORS(app)  # Allow frontend (React) to call API

# Configure rotating log file
log_handler = RotatingFileHandler('server.log', maxBytes=1000000, backupCount=3)
log_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
log_handler.setFormatter(formatter)

# Configure console logging
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)
console_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)
logger.addHandler(console_handler)

@app.route('/process-json', methods=['POST'])
def process_json():
    try:
        data = request.json
        logger.info("Received data: %s", data)

        transcript = data.get("transcript", [])

        # Dummy processing logic
        summary = ["This is a sample summary."]
        actions = ["This is a sample action."]
        decisions = ["This is a sample decision."]

        response = {
            "summary": summary,
            "actions": actions,
            "decisions": decisions
        ***REMOVED***
        logger.info("Response: %s", response)
        return jsonify(response)

    except Exception as e:
        logger.error("Error processing request: %s", str(e))
        return jsonify({"error": "Internal Server Error"***REMOVED***), 500

if __name__ == '__main__':
    app.run(debug=True)
