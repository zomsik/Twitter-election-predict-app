# -*- coding: utf-8 -*-
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from model.cardiffnlpSentiment import calculateCardiffnlpSentiment
from tweets.get_tweets import get_tweets
from model.ownSentiment import predict
from model.textblobSentiment import getTextBlobPredict
from server.SentimentComparisonModel import SentimentComparisonModel
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# Strona główna z wyborem tweetów
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Strona z wynikiem oceny pojedynczego tweeta
@app.post("/analyze_tweet", response_class=HTMLResponse)
async def analyze_tweet(request: Request):
    form_data = await request.form()
    tweet_text = form_data.get("tweet_text")
    cardiffnlpRanking, cardiffnlpScore = calculateCardiffnlpSentiment(tweet_text)
    textblobRanking, textblobScore = getTextBlobPredict(tweet_text)
    ownRanking, ownScore = predict(tweet_text)
    
    return templates.TemplateResponse("result_tweet.html", {"request": request, "tweet": tweet_text, 
                                                "ranking_cardiffnlp_model": cardiffnlpRanking, "sentiment_cardiffnlp_model": cardiffnlpScore,
                                                "ranking_textblob_model": textblobRanking, "sentiment_textblob_model": textblobScore,
                                                "ranking_own_model": ownRanking, "sentiment_own_model": ownScore})
                                                            


# Strona z wynikami webscrapowania tweetów
@app.post("/scrape_tweets", response_class=HTMLResponse)
async def scrape_tweets(request: Request):
    form_data = await request.form()
    num_tweets = form_data.get("num_tweets")
    outputTweets = []
    
    scraped_tweets = get_tweets("#biden", num_tweets)

    pos = neu = neg = 0

    for tweet in scraped_tweets:
        text = str(tweet.text)
        cardiffnlpRanking, cardiffnlpScore = calculateCardiffnlpSentiment(text)
        textblobRanking, textblobScore = getTextBlobPredict(text)
        ownRanking, ownScore = predict(text)
        if ownRanking == "positive":
            pos+=1
        elif ownRanking == "neutral":
            neu+=1
        elif ownRanking == "negative":
            neg+=1
        
        outputTweets.append(SentimentComparisonModel(text, cardiffnlpRanking, cardiffnlpScore, 
                                           textblobRanking, textblobScore, 
                                           ownRanking, ownScore))
    
        
    webscrapResult = "Na podstawie webscrapowania tweetów można stwierdzić, że "

    if pos >= neu and pos > neg:
        webscrapResult += "Biden MA SZANSĘ na ponowną reelekcję z uwagi na przeważające tweety o pozytywnym sentymencie."
    elif neu > pos and neu > neg:
        webscrapResult += "NIE WIADOMO czy Biden ma szanse na ponowną reelekcję z uwagi na przeważające tweety o neutralnym sentymencie."
    elif neg >= neu and neg > pos:
        webscrapResult += "Biden NIE MA SZANSY na ponowną reelekcję z uwagi na przeważające tweety o negatywnym sentymencie." 
    else:
        webscrapResult += "NIE WIADOMO czy Biden ma szanse na ponowną reelekcję z uwagi na duże podział tweetów względem ich sentymentu."

    return templates.TemplateResponse("result_scraped.html", {"request": request, "tweets": outputTweets, "webscrapResult": webscrapResult})