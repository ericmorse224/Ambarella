# File: test_ner.py
# Author: Eric Morse
# Date: May 11th, 2025
#
# Description:
#   This script demonstrates how to extract PERSON entities from a block of text
#   using NLTK's named entity recognition (NER) capabilities. It provides both an
#   advanced chunk-based NER approach and a simpler regex-based fallback. Titles
#   (e.g., "Dr.", "Mr.") are also considered as prefixes for names.
#
#   Usage:
#     - Run this file as a standalone script to see entity extraction on a sample text.
#     - Main dependencies: nltk
#
#   Notes:
#     - Make sure to download necessary NLTK resources before use:
#         nltk.download('punkt')
#         nltk.download('averaged_perceptron_tagger')
#         nltk.download('maxent_ne_chunker')
#         nltk.download('words')

import nltk
from typing import List, Dict, Any

# Set of known title prefixes for people (used for enhanced PERSON detection)
TITLE_PREFIXES = {"Mr", "Ms", "Mrs", "Dr", "Prof", "Sir", "Madam"}

def extract_probable_people(text: str) -> List[str]:
    """
    Uses a regex pattern to extract capitalized words or pairs (potential names)
    from the input text as a simple backup/fallback for people extraction.
    
    Args:
        text (str): Input text to search for names.
        
    Returns:
        List[str]: List of probable person names.
    """
    import re
    pattern = re.compile(r'\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)\b')
    return pattern.findall(text)

def extract_entities(text: str) -> List[Dict[str, Any]]:
    """
    Extracts PERSON entities from text using NLTK's named entity chunker.
    Enhances extraction by including recognized titles as prefixes, then adds
    fallback names found via regex if not already present.

    Args:
        text (str): The input text to analyze.
    
    Returns:
        List[Dict[str, Any]]: A list of entity dicts with keys 'text' and 'entity_type'.
    """
    # Tokenize and POS tag the text
    tokens = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(tokens)
    chunked = nltk.ne_chunk(pos_tags, binary=False)

    entities = []
    i = 0
    while i < len(chunked):
        subtree = chunked[i]
        if hasattr(subtree, 'label') and subtree.label() == 'PERSON':
            person_tokens = [token for token, pos in subtree.leaves()]
            # Search backwards for a title (e.g., "Dr.", "Mr.")
            j = i - 1
            while j >= 0:
                prev = chunked[j]
                # Only add title if previous is a token (not a subtree) and matches title list
                if not hasattr(prev, 'label') and prev[0].rstrip('.').capitalize() in TITLE_PREFIXES:
                    person_tokens.insert(0, prev[0])
                    j -= 1
                else:
                    break
            entity_text = " ".join(person_tokens)
            entities.append({"text": entity_text, "entity_type": "PERSON"})
            i += 1
        else:
            i += 1

    # Fallback: add other probable people from regex extraction (if not already present)
    probable_people = extract_probable_people(text)
    existing_names = set(e['text'].lower() for e in entities)
    for p in probable_people:
        if p.lower() not in existing_names:
            entities.append({"text": p, "entity_type": "PERSON"})

    return entities

if __name__ == "__main__":
    # Example usage with a test string
    test_text = "Dr. Alice and Mr. Bob Lee discussed the project. Carol Jones will follow up."

    entities = extract_entities(test_text)
    print("Extracted entities:")
    for e in entities:
        print(f"  {e['entity_type']}: {e['text']}")
