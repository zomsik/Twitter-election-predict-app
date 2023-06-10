# -*- coding: utf-8 -*-
from keras.models import load_model 
import pickle
from joblib import dump, load 
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from sklearn.preprocessing import LabelEncoder


model = load_model("data/model.h5")

model.summary()

w2v_model = load_model("data/model.w2v")

en = load('data/encoder.pkl')

tokenizer = pickle.load(open('data/tokenizer.pkl', 'rb'))
encoder = pickle.load(open('data/encoder.pkl', 'rb'))

with open('data/tokenizer.pkl', 'rb') as handle:
    saa = pickle.load(handle)
    
    
    

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

        
a = predict("dupa cycki")