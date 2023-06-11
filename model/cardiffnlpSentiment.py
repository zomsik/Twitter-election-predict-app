from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
import numpy as np
from scipy.special import softmax
import csv
import urllib.request
from sklearn.preprocessing import MinMaxScaler
import os

MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = None
model = None
labels = []

def preprocess(text):
    new_text = []
 
 
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)


def load_or_download_model():
    global tokenizer, model

    if os.path.exists(MODEL):
        tokenizer = AutoTokenizer.from_pretrained(MODEL)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    else:
        download_model()


def download_model():
    global tokenizer, model
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    tokenizer.save_pretrained(MODEL)
    model.save_pretrained(MODEL)
        
    
def load_labels():
    global labels
    mapping_link = "https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/sentiment/mapping.txt"
    with urllib.request.urlopen(mapping_link) as f:
        html = f.read().decode('utf-8').split("\n")
        csvreader = csv.reader(html, delimiter='\t')
        labels = [row[1] for row in csvreader if len(row) > 1]


def calculateCardiffnlpSentiment(text):
    global tokenizer, model, labels
    if tokenizer is None or model is None:
        load_or_download_model()
        
    if not labels:
        load_labels()

    text = preprocess(text)
    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()

    scores = softmax(scores)

    ranking = np.argsort(scores)
    ranking = ranking[::-1]

    return labels[ranking[0]], scores[ranking[0]]