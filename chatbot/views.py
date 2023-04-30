from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import tensorflow as tf
import json
import random
import pickle
from .nltk_utils import tokenize, lemmatize, bag_of_words
from tensorflow.keras.models import load_model

with open("/home/divpugo/Middlesex/chatbot/intents.json", "r") as file:
    intents = json.load(file)

model = load_model("/home/divpugo/Middlesex/chatbot/chatbot_model.h5")

with open("/home/divpugo/Middlesex/chatbot/tags.pkl", "rb") as f_tags:
    all_tags = pickle.load(f_tags)

with open("/home/divpugo/Middlesex/chatbot/words.pkl", "rb") as f_words:
    all_words = pickle.load(f_words)

@csrf_exempt
@require_POST
def chatbot(request):
    user_message = request.POST.get('message')
    chatbot_response = get_chatbot_response(user_message)
    return JsonResponse({'message': chatbot_response})

def get_chatbot_response(user_message):
    # Preprocess the user message
    user_message = tokenize(user_message)
    user_message = [lemmatize(word) for word in user_message]
    user_message = bag_of_words(user_message, all_words)
    input_sequence = tf.expand_dims(user_message, 0)

    # Get the chatbot's response
    prediction = model.predict(input_sequence)
    predicted_index = tf.argmax(prediction, axis=-1).numpy()[0]
    tag = all_tags[predicted_index]

    for intent in intents['intents']:
        if tag == intent["tag"]:
            response = random.choice(intent['responses'])
            break

    return response
