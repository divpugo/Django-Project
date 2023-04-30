import json
import pytest
from chat import predict_class, get_response

# Load the necessary data for testing
with open("intents.json", "r") as f:
    intents = json.load(f)

def test_predict_class_valid_input():
    # Test the predict_class function with valid input
    input_sentence = "hello"
    predictions = predict_class(input_sentence)
    assert len(predictions) > 0

def test_predict_class_invalid_input():
    # Test the predict_class function with invalid input
    input_sentence = "@$%&*"
    predictions = predict_class(input_sentence)
    unrecognized_intent = all([prediction['intent'] == 'unrecognized' for prediction in predictions])
    assert unrecognized_intent

def test_get_response_empty_intent():
    # Test the get_response function with an empty intent
    intent = []
    response = get_response(intent, intents)
    assert response == "I'm sorry, I didn't understand your input. Please try again with a different input."
def test_get_response_valid_intent():
    # Test the get_response function with a valid intent
    intent = [{"intent": "greeting", "probability": "0.9"}]
    response = get_response(intent, intents)
    assert response is not None

def test_get_response_multiple_intents():
    # Test the get_response function with multiple intents
    intent = [{"intent": "greeting", "probability": "0.9"}, {"intent": "goodbye", "probability": "0.8"}]
    response = get_response(intent, intents)
    assert response is not None
