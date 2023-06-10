import requests
import json 
import os
from tweets.Tweet import Tweet

def get_tweets(hashtag, count):

    tweet_list = []


    api_key = os.getenv("scrapperApi")

    payload = {
       'api_key': api_key,
       'num': 5,
       'query': hashtag,
       'time_period': '1D'
    }

    responseBytes = requests.get('https://api.scraperapi.com/structured/twitter/search', params=payload)
    responseData = responseBytes.content.decode('utf-8')



    
    if responseData is None or "Request failed" in responseData or "Unauthorized request" in responseData:
        return tweet_list
    
    print(responseData)
    
    responseJson = json.loads(responseData)
    
    for tweet in responseJson['tweets']:
        
        if 'user' not in tweet or 'tweet_id' not in tweet:
            continue
        
        payloadTweet = {
           'api_key': api_key,
           'user': tweet['user'],
           'id': tweet['tweet_id']
        }
        
        responseBytesTweet = requests.get('https://api.scraperapi.com/structured/twitter/tweet', params=payloadTweet)
        
        if responseBytesTweet.content is None:
            continue
        
        responseDataTweet = responseBytesTweet.content.decode('utf-8')
        
        if responseDataTweet is None or "Request failed" in responseDataTweet or "Unauthorized request" in responseDataTweet:
            continue
        
        responseJsonTweet = json.loads(responseDataTweet)
        
        if 'text' not in responseJsonTweet:
            continue
        
        
        if 'date' not in responseJsonTweet:
            responseJsonTweet['date'] = None
        if 'is_reply' not in responseJsonTweet:
            responseJsonTweet['is_reply'] = None
        if 'likes' not in responseJsonTweet:
            responseJsonTweet['likes'] = None
        if 'is_retweet' not in responseJsonTweet:
            responseJsonTweet['is_retweet'] = None
        if 'user_verified' not in responseJsonTweet:
            responseJsonTweet['user_verified'] = None
        if 'views' not in responseJsonTweet:
            responseJsonTweet['views'] = None    
        if 'retweets' not in responseJsonTweet:
            responseJsonTweet['retweets'] = None   
        if 'real_name' not in responseJsonTweet:
            responseJsonTweet['real_name'] = None   
            
        """tweet_list.append(Tweet(responseJsonTweet['date'],
                                responseJsonTweet['is_reply'],
                                responseJsonTweet['is_retweet'],
                                responseJsonTweet['likes'],
                                responseJsonTweet['real_name'],
                                tweet['user'],
                                tweet['tweet_id'],
                                responseJsonTweet['text'],
                                responseJsonTweet['user_verified'],
                                responseJsonTweet['views'],
                                responseJsonTweet['retweets']))"""
        tweet_list.append(responseJsonTweet)
        
        if len(tweet_list) >= count:
            break

    return tweet_list
