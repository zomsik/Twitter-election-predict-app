# -*- coding: utf-8 -*-
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from textblob import TextBlob

from data.get_tweets import get_tweets

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    tweets = get_tweets(hashtag="#biden", count=10)
    html_content = "<h2>Recent Tweets</h2>"
    for tweet in tweets:
        html_content += f"<p>{tweet['text']}</p>"

        blob = TextBlob(tweet['text'])
        sentiment = blob.sentiment.polarity

        if sentiment > 0:
            html_content += '<p style="color: green">Positive</p>'
        elif sentiment < 0:
            html_content += '<p style="color: red">Negative</p>'
        else:
            html_content += '<p style="color: blue">Neutral</p>'
            
            
        
    return html_content