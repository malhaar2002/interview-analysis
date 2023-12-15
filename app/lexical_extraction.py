import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

liwc_categories = {
    'posEmotion': ['hope', 'improve', 'kind', 'love', 'happy', 'pretty', 'good', 'joy', 'excited', 'optimistic', 'satisfied', 'confident', 'enthusiastic', 'pleased', 'grateful'],
    'Cognitive': ['cause', 'know', 'ought', 'learn', 'make', 'notice', 'understand', 'think', 'reason', 'realize', 'analyze', 'comprehend', 'ponder', 'contemplate', 'reflect'],
    'Work': ['project', 'study', 'thesis', 'class', 'work', 'university', 'job', 'employment', 'career', 'task', 'interview', 'meeting', 'resume', 'deadline', 'position'],
    'Tentative_Language': ['maybe', 'perhaps', 'guess', 'possibly', 'potentially', 'could', 'might', 'assuming', 'probable', 'likely', 'feasible', 'possible', 'hypothetical', 'uncertain', 'tentative'],
    'Filler_Words': ['ah', 'Ah', 'Ahh', 'ahh', 'uhm', 'Uhm', 'Uhmmm', 'um', 'Um', 'uh', 'Uhh', 'Umm', 'ummm', 'Mmhmm', 'Uhhhh', 'Hmm', 'uhhhh', 'uhh', 'umm', 'Uh']
}

# Initialize the Porter Stemmer
def extract_lexical_features(response):
    stemmer = PorterStemmer()

    tokens = word_tokenize(response)
    tokens = [stemmer.stem(word.lower()) for word in tokens]

    # Initialize category counts for the current response
    category_counts = {category: 0 for category in liwc_categories.keys()}

    # Count occurrences of stemmed words in LIWC categories for the current response
    for word in tokens:
        for category, category_words in liwc_categories.items():
            if word in [stemmer.stem(category_word) for category_word in category_words]:
                category_counts[category] += 1

    # Optionally, perform sentiment analysis on the response (VADER sentiment analysis)
    # Store the category counts and sentiment scores for the current response
    return category_counts