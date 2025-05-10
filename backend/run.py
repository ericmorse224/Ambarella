from flask import Flask, request, jsonify
from flask_cors import CORS
import nltk
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
from nltk.tokenize import sent_tokenize



app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"***REMOVED******REMOVED***)

@app.route('/process-json', methods=['POST'])
def process_json():
    data = request.json
    transcript = data.get("transcript", [])
    full_text = " ".join([segment["text"] for segment in transcript])

    sentences = sent_tokenize(full_text)

    summary = []
    actions = []
    decisions = []

    for sentence in sentences:
        if "decided" in sentence.lower():
            decisions.append(sentence)
        elif any(word in sentence.lower() for word in ["will", "must", "should", "needs to"]):
            actions.append(sentence)
        else:
            summary.append(sentence)

    return jsonify({
        "summary": summary,
        "actions": actions,
        "decisions": decisions
    ***REMOVED***)

if __name__ == '__main__':
    app.run(debug=True)
