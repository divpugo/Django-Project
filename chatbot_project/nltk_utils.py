from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import numpy as np

lemmatizer = WordNetLemmatizer()

def tokenize(sentence):
    return word_tokenize(sentence)

def lemmatize(word):
    return lemmatizer.lemmatize(word.lower())

def bag_of_words(tokenized_sentence, words):
    sentence_words = [lemmatize(word) for word in tokenized_sentence]
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in sentence_words:
            bag[idx] = 1.0
    return bag
