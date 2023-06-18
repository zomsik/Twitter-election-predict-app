# -*- coding: utf-8 -*-
import os
import pickle
from model.newModel import createNewModel
from keras.utils import pad_sequences
from keras.models import load_model 

model = None
tokenizer = None

def loadModel():
    global model, tokenizer
    
    if os.path.exists('data/model.h5') and os.path.exists('data/tokenizer.pkl'):
        model = load_model("data/model.h5")
        tokenizer = pickle.load(open('data/tokenizer.pkl', 'rb'))
    else:
        model, tokenizer = createNewModel()


def decode_sentiment(score):
    label = "neutral"
    if score <= 1/3:
        label = "negative"
    elif score >= 2/3:
        label = "positive"

    return label

def predict(text):
    
    if tokenizer is not None and model is not None:
        x_test = pad_sequences(tokenizer.texts_to_sequences([text]), maxlen=300)
        score = model.predict([x_test])[0]
        label = decode_sentiment(score)
        return label, float(score)
    else:
        loadModel()
        return predict(text)
        
