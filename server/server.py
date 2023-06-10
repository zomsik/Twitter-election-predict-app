# -*- coding: utf-8 -*-
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from model.sentiment import calculateSentiment
from data.get_tweets import get_tweets

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# Strona główna z menu
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Strona z wynikiem oceny pojedynczego tweeta
@app.post("/analyze_tweet", response_class=HTMLResponse)
async def analyze_tweet(request: Request):
    form_data = await request.form()
    tweet_text = form_data.get("tweet_text")


    ranking, score = calculateSentiment(tweet_text)
    # Tutaj dodaj kod do oceny pojedynczego tweeta
    # Możesz użyć wcześniej omówionego modelu do analizy sentymentu

    return templates.TemplateResponse("result_tweet.html", {"request": request, "tweet": tweet_text,  "sentiment_pretrained_model": 0.34, "sentiment_own_model": score, "ranking_own_model": ranking})

# Strona z wynikami webscrapowania tweetów
@app.post("/scrape_tweets", response_class=HTMLResponse)
async def scrape_tweets(request: Request):
    form_data = await request.form()
    num_tweets = form_data.get("num_tweets")

    # Tutaj dodaj kod do webscrapowania tweetów na podstawie podanej liczby
    # Możesz użyć odpowiednich bibliotek, takich jak BeautifulSoup czy Scrapy

    scraped_tweets = [...]  # Przykładowa lista zebranych tweetów

    return templates.TemplateResponse("result_scraped.html", {"request": request, "tweets": scraped_tweets})






@app.get("/s", response_class=HTMLResponse)
async def inssdex(request: Request):
    #tweets = get_tweets(hashtag="#biden", count=5)
    tweets = []
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