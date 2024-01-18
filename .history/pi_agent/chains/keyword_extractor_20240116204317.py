import re
from collections import Counter
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

class KeywordExtractor:
    def __init__(self):
        # Initialize any required components, such as NLP models or configurations
        pass

    def extract_keywords(self, text, top_k=5):
        # Preprocess the text: remove punctuation, convert to lowercase, and split into words
        words = re.findall(r'\w+', text.lower())
        # Filter out stop words

