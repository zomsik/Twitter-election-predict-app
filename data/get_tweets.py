import requests
import json 
import os
from data.Tweet import Tweet

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
        
        if 'user' not in tweet or 'tweet_id' not in tweet:
            continue
        
        payload = {
           'api_key': api_key,
           'user': tweet['user'],
           'id': tweet['tweet_id']
        }
        
        responseBytes = requests.get('https://api.scraperapi.com/structured/twitter/tweet', params=payload)
        responseData = responseBytes.content.decode('utf-8')
        responseJson = json.loads(responseData)
        
        if 'text' not in responseJson:
            continue
        
        
        if 'date' not in responseJson:
            responseJson['date'] = None
        if 'is_reply' not in responseJson:
            responseJson['is_reply'] = None
        if 'likes' not in responseJson:
            responseJson['likes'] = None
        if 'is_retweet' not in responseJson:
            responseJson['is_retweet'] = None
        if 'user_verified' not in responseJson:
            responseJson['user_verified'] = None
        if 'views' not in responseJson:
            responseJson['views'] = None    
        if 'retweets' not in responseJson:
            responseJson['retweets'] = None   
        if 'real_name' not in responseJson:
            responseJson['real_name'] = None   
            
        tweet_list.append(Tweet(responseJson['date'],
                                responseJson['is_reply'],
                                responseJson['is_retweet'],
                                responseJson['likes'],
                                responseJson['real_name'],
                                tweet['user'],
                                tweet['tweet_id'],
                                responseJson['text'],
                                responseJson['user_verified'],
                                responseJson['views'],
                                responseJson['retweets']))

    return tweet_list
