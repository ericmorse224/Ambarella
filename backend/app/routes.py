from flask import Blueprint, request, jsonify
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from nltk.tokenize import sent_tokenize
from app.utils.logger import logger

main = Blueprint('main', __name__)

@main.route('/process-json', methods=['POST'])
def process_json():
    try:
        data = request.get_json()
        transcript_text = " ".join([turn['text'] for turn in data['transcript']])
        logger.info('Received transcript for processing.')

        parser = PlaintextParser.from_string(transcript_text, Tokenizer('english'))
        summarizer = LsaSummarizer()
        summary = [str(sentence) for sentence in summarizer(parser.document, 5)]

        actions = [s for s in sent_tokenize(transcript_text) if 'will' in s or 'must' in s]
        decisions = [s for s in sent_tokenize(transcript_text) if 'decided' in s or 'agreed' in s]

        return jsonify({
            'summary': summary,
            'actions': actions,
            'decisions': decisions
        })
    except Exception as e:
        logger.error(f'Error processing transcript: {str(e)}')
        return jsonify({'error': str(e)}), 500

