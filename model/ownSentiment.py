# -*- coding: utf-8 -*-
import os
import pickle
from model.newModel import createNewModel
from keras.utils import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.models import load_model 

model = None
w2v_model = None
tokenizer = None
encoder = None

def loadModel():
    global model, w2v_model, tokenizer, encoder
    
    if os.path.exists('data/model.h5') and os.path.exists('data/model.w2v') and os.path.exists('data/tokenizer.pkl') and os.path.exists('data/encoder.pkl'):
        model = load_model("data/model.h5")
        #w2v_model = load_model("data/model.w2v")
        tokenizer = pickle.load(open('data/tokenizer.pkl', 'rb'))
        #encoder = pickle.load(open('data/encoder.pkl', 'rb'))
    else:
        #model, w2v_model, tokenizer, encoder = createNewModel()
        print("wczytaj")
        
        

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
        
