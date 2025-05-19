"""
setup.py

NLTK Data Download Script for AI Meeting Summarizer Backend.

Created by Eric Morse
Date: 2024-05-18

This script downloads required NLTK corpora and models for the NLP pipeline.
Run this file to ensure all NLTK data dependencies are available.

Usage:
    python setup.py
"""

import nltk

# Download essential NLTK corpora/models for NLP analysis.
nltk.download('punkt')                    # Tokenizer for sentences and words
nltk.download('maxent_ne_chunker')        # Named Entity Chunker (NER)
nltk.download('words')                    # Vocabulary/corpus for NE Chunker
nltk.download('averaged_perceptron_tagger')  # Part-of-speech tagger
nltk.download('averaged_perceptron_tagger_eng') # English language speech tagger
# You can add other downloads here if your pipeline grows in the future.
