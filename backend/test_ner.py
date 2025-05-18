import nltk
from typing import List, Dict, Any

# Make sure to download these once before running:
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')

TITLE_PREFIXES = {"Mr", "Ms", "Mrs", "Dr", "Prof", "Sir", "Madam"}

def extract_probable_people(text: str) -> List[str]:
    import re
    pattern = re.compile(r'\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)\b')
    return pattern.findall(text)

def extract_entities(text: str) -> List[Dict[str, Any]]:
    tokens = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(tokens)
    chunked = nltk.ne_chunk(pos_tags, binary=False)

    entities = []
    i = 0
    while i < len(chunked):
        subtree = chunked[i]
        if hasattr(subtree, 'label') and subtree.label() == 'PERSON':
            person_tokens = [token for token, pos in subtree.leaves()]
            # Look backwards for titles
            j = i - 1
            while j >= 0:
                prev = chunked[j]
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

    # Add probable people fallback
    probable_people = extract_probable_people(text)
    existing_names = set(e['text'].lower() for e in entities)
    for p in probable_people:
        if p.lower() not in existing_names:
            entities.append({"text": p, "entity_type": "PERSON"})

    return entities

if __name__ == "__main__":
    test_text = "Dr. Alice and Mr. Bob Lee discussed the project. Carol Jones will follow up."

    entities = extract_entities(test_text)
    print("Extracted entities:")
    for e in entities:
        print(f"  {e['entity_type']}: {e['text']}")
