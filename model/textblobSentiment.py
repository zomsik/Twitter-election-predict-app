# -*- coding: utf-8 -*-
from textblob import TextBlob

def getTextBlobPredict(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    
    if sentiment > 0:
        ranking = "positive"
    elif sentiment < 0:
        ranking = "negative"
    else:
        ranking = "neutral"
    
    sentiment = (sentiment + 1) / 2

    return ranking, sentiment