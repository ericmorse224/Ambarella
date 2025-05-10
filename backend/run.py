from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])  # Allow only frontend dev origin

@app.route('/process-json', methods=['POST'])
def process_json():
    data = request.json
    # your processing logic here...
    return jsonify({
        "summary": ["This is a test summary."],
        "actions": ["User will do something important."],
        "decisions": ["It was decided to continue the project."]
    ***REMOVED***)

if __name__ == '__main__':
    app.run(debug=True)
