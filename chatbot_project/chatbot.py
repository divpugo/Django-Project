import json
import numpy as np
import tensorflow as tf
import nltk
import pickle
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, Reshape, Flatten
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from nltk_utils import tokenize, lemmatize, bag_of_words

nltk.download('punkt')
nltk.download('wordnet')

# Load the intents dataset
with open("intents.json", "r") as f:
    intents = json.load(f)

all_words = []
tags = []
xy = []

# Preprocess the intents dataset
for intent in intents["intents"]:
    tag = intent["tag"]
    tags.append(tag)
    for pattern in intent["patterns"]:
        w = tokenize(pattern)
        all_words.extend(w)
        xy.append((w, tag))

# Apply lemmatization and remove duplicates
all_words = [lemmatize(w) for w in all_words]
all_words = sorted(set(all_words))
tags = sorted(set(tags))

# Create training data
X_train = []
y_train = []

for (pattern_sentence, tag) in xy:
    bag = bag_of_words(pattern_sentence, all_words)
    X_train.append(bag)

    label = tags.index(tag)
    y_train.append(label)

X_train = np.array(X_train)
y_train = np.array(y_train)

# One-hot encode the labels
onehot_encoder = OneHotEncoder(sparse=False)
y_train = y_train.reshape(len(y_train), 1)
y_train = onehot_encoder.fit_transform(y_train)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# Define the neural network model
model = Sequential()
model.add(Dense(128, input_shape=(len(X_train[0]),), activation="relu"))
model.add(Dropout(0.5))
model.add(Reshape((1, 128)))  
model.add(LSTM(64, return_sequences=True))
model.add(Dropout(0.5))
model.add(Flatten())  
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(len(y_train[0]), activation="softmax"))

# Compile and train the model
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
model.fit(X_train, y_train, epochs=200, batch_size=32, validation_data=(X_test, y_test))

# Save the trained model and other necessary files
model.save("chatbot_model.h5")
with open("words.pkl", "wb") as f:
    pickle.dump(all_words, f)

with open("tags.pkl", "wb") as f:
    pickle.dump(tags, f)
