# backend/utils/nlp_utils.py
import re
import nltk
from nltk.tokenize import word_tokenize

# Uncomment the next line if running for the first time
nltk.download('punkt')

def process_message(message: str) -> str:
    tokens = word_tokenize(message)
    pattern = re.compile(r'help', re.IGNORECASE)
    help_keywords = [word for word in tokens if pattern.search(word)]
    
    if help_keywords:
        return "It looks like you might need some help. How can I assist you further?"
    else:
        return f"You said: {message}"
