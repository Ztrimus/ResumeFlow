'''
-----------------------------------------------------------------------
File: metrics.py
Creation Time: Jan 13th 2024, 8:42 pm
Author: Saurabh Zinjad
Developer Email: saurabhzinjad@gmail.com
Copyright (c) 2023-2024 Saurabh Zinjad. All rights reserved | https://github.com/Ztrimus
-----------------------------------------------------------------------
'''
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
import re

def remove_urls(list_of_strings):
    """Removes strings containing URLs from a list using regular expressions."""
    filtered_list = [string for string in list_of_strings if not re.search(r"https?://\S+", string)]
    return filtered_list

def overlap_coefficient(document1: str, document2: str) -> float:
    """Calculate the overlap coefficient between two documents.

    The overlap coefficient is a measure of the overlap between two sets, 
    and is defined as the size of the intersection divided by the smaller 
    of the size of the two sets.

    Args:
        document1 (str): The first document.
        document2 (str): The second document.

    Returns:
        float: The overlap coefficient between the two documents.
    """    
    # List the unique words in a document
    words_in_document1 = set(normalize_text(document1))
    words_in_document2 = set(normalize_text(document2))

    # Find the intersection of words list of document1 & document2
    intersection = words_in_document1.intersection(words_in_document2)

    # Calculate overlap coefficient
    try:
        overlap_coefficient = float(len(intersection)) / min(len(words_in_document1), len(words_in_document2))
    except ZeroDivisionError:
        overlap_coefficient = 0.0

    return overlap_coefficient
    
def jaccard_similarity(document1: str, document2: str) -> float:
    """Calculate the Jaccard similarity between two documents.

    The Jaccard similarity is a measure of the similarity between two sets, 
    and is defined as the size of the intersection divided by the size of 
    the union of the two sets.

    Args:
        document1 (str): The first document.
        document2 (str): The second document.

    Returns:
        float: The Jaccard similarity between the two documents.
    """    
    # List the unique words in a document
    words_in_document1 = set(normalize_text(document1))
    words_in_document2 = set(normalize_text(document2))

    # Find the intersection of words list of document1 & document2
    intersection = words_in_document1.intersection(words_in_document2)

    # Find the union of words list of document1 & document2
    union = words_in_document1.union(words_in_document2)
        
    # Calculate Jaccard similarity score 
    try:
        jaccard_similarity = float(len(intersection)) / len(union)
    except ZeroDivisionError:
        jaccard_similarity = 0.0

    return jaccard_similarity

def normalize_text(text: str) -> list:
    """Normalize the input text.

    This function tokenizes the text, removes stopwords and punctuations, 
    and applies stemming.

    Args:
        text (str): The text to normalize.

    Returns:
        list: The list of normalized words.
    """    
    # Step 1: Tokenization
    words = word_tokenize(text)

    # Step 2: Data Cleaning - Remove Stopwords and Punctuations 
    words = [re.sub('[^a-zA-Z]', '', word).lower() for word in words]

    # Step 3: Remove empty tokens
    words = [word for word in words if len(word)] 

    # Step 4: Remove Stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]

    # Step 5: Stemming
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]

    #STEP 3 : LEMMATIZATION
    # lemmatizer=WordNetLemmatizer()
    # words=[lemmatizer.lemmatize(word) for word in words]
    
    return words 