import requests
import json 
import csv
import os


class Tweet:
    def __init__(self, date, isReply, isRetweet, likes, username, text, isVerified):
        self.date = date
        self.username = username
        self.text = text.replace('\n', '')
        self.likes = likes
        self.isReply = isReply
        self.isRetweet = isRetweet
        self.isVerified = isVerified

    def __str__(self):
        return f"{self.username}: {self.text}, {self.likes}"


def get_tweets(hashtag, count):

    api_key = os.getenv("scrapperApi")

    payload = {
       'api_key': api_key,
       'num': count,
       'query': hashtag,
       'time_period': '1D'
    }

    responseBytes = requests.get('https://api.scraperapi.com/structured/twitter/search', params=payload)

    responseData = responseBytes.content.decode('utf-8')
    
    responseJson = json.loads(responseData)
    
    tweet_list = []

    for tweet in responseJson['tweets']:
        payload = {
           'api_key': api_key,
           'user': tweet['user'],
           'id': tweet['tweet_id']
        }
        responseBytes = requests.get('https://api.scraperapi.com/structured/twitter/tweet', params=payload)
        responseData = responseBytes.content.decode('utf-8')
        responseJson = json.loads(responseData)
        
        tweet_list.append(Tweet(responseJson['date'],
                                responseJson['is_reply'],
                                responseJson['is_retweet'],
                                responseJson['likes'],
                                responseJson['real_name'],
                                responseJson['text'],
                                responseJson['user_verified']))

    return tweet_list
