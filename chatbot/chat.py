import pickle
import json
import random
import numpy as np
from tensorflow.keras.models import load_model
from nltk_utils import bag_of_words, tokenize
import re

def predict_class(sentence):
    # Remove non-alphabetic characters and convert to lowercase
    clean_sentence = re.sub(r'[^a-zA-Z\s]', '', sentence).lower()

    if not clean_sentence.strip():
        return [{"intent": "unrecognized", "probability": "1"}]

    sentence_bag = bag_of_words(tokenize(clean_sentence), words)
    res = model.predict(np.array([sentence_bag]))[0]
    threshold = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > threshold]

    if not results:
        return [{"intent": "unrecognized", "probability": "1"}]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": tags[r[0]], "probability": str(r[1])})
    return return_list



def get_response(intents_list, intents_json):
    if len(intents_list) == 0 or intents_list[0]['intent'] == 'unrecognized':
        return "I'm sorry, I didn't understand your input. Please try again with a different input."

    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result



# Load the necessary data
with open("intents.json", "r") as f:
    intents = json.load(f)

with open("words.pkl", "rb") as f:
    words = pickle.load(f)

with open("tags.pkl", "rb") as f:
    tags = pickle.load(f)

# Load the trained model
model = load_model("chatbot_model.h5")

def start_chat():
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break

        predictions = predict_class(user_input)
        response = get_response(predictions, intents)
        print("Chatbot:", response)

if __name__ == "__main__":
    start_chat()

