### backend/app/summarization.py
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer


def summarize_transcript(transcript):
    full_text = " ".join([entry["text"] for entry in transcript])
    parser = PlaintextParser.from_string(full_text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary_sentences = summarizer(parser.document, 3)
    return [str(sentence) for sentence in summary_sentences]
