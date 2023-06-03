# -*- coding: utf-8 -*-

class Tweet:
    def __init__(self, date, isReply, isRetweet, likes, username, userlink, tweetId, text, isVerified, views, retweets):
        self.date = date
        self.username = username
        self.userlink = userlink
        self.tweetId = tweetId
        self.text = text.replace('\n', '')
        self.likes = likes
        self.isReply = isReply
        self.isRetweet = isRetweet
        self.isVerified = isVerified
        self.views = views
        self.retweets = retweets

    def __str__(self):
        return f"{self.username}: {self.text}, {self.views}, {self.likes}"

