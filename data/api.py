# -*- coding: utf-8 -*-

import requests
import json 
import csv
import os

api_key = os.getenv("scrapperApi")

payload = {
   'api_key': api_key,
   'num': '50',
   'query': '#biden',
   'time_period': '2D'
}


responseBytes = requests.get('https://api.scraperapi.com/structured/twitter/search', params=payload)

responseData = responseBytes.content.decode('utf-8')
responseData1 = responseData.replace('"', '')
responseData1 = responseData1.replace('”', '')
responseJson = json.loads(responseData)

tweets = responseJson['tweets']


myFile = open('demo_file.csv', 'w', encoding='UTF8', newline='')
writer = csv.writer(myFile)
writer.writerow(['TweetId','User','Title','Text','Link','ScraperLink','ScraperTweetLink','ScraperRepliesLink'])
for dictionary in tweets:
    writer.writerow(dictionary.values())
myFile.close()





payload = {
   'api_key': api_key,
   'user': 'IndiaToday',
   'id': 1664478877647773701
}

responseBytes = requests.get('https://api.scraperapi.com/structured/twitter/tweet', params=payload)

responseData = responseBytes.content.decode('utf-8')
responseJson = json.loads(responseData)