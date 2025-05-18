# setup_nltk.py
import nltk
nltk.download('all')
nltk.download('punkt')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')
# optionally you can manually run python -c "import nltk; nltk.download('all')"
# or python -m nltk.downloader averaged_perceptron_tagger