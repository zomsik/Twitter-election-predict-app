# -*- coding: utf-8 -*-
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from textblob import TextBlob
from model.sentiment import calculateSentiment
from data.get_tweets import get_tweets

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    tweets = get_tweets(hashtag="#biden", count=5)
    html_content = "<h2>Recent Tweets</h2>"
    for tweet in tweets:
        html_content += f"<p>{tweet.text}</p>"
        ranking, score = calculateSentiment(tweet.text)
        
        if ranking == "positive":
            html_content += '<p style="color: green">Positive: ' + score*100 + '%</p>'
        elif ranking == "neutral":
            html_content += '<p style="color: blue">Neutral: ' + score*100 + '%</p>'
        elif ranking == "negative":
            html_content += '<p style="color: red">Negative: ' + score*100 + '%</p>'
            
        
    return html_content