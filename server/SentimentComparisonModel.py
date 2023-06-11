# -*- coding: utf-8 -*-

class SentimentComparisonModel:
    def __init__(self, text, cardiffnlpRanking, cardiffnlpScore, textblobRanking, textblobScore, ownRanking, ownScore):
        self.text = text
        self.cardiffnlpRanking = cardiffnlpRanking
        self.cardiffnlpScore = cardiffnlpScore
        self.textblobRanking = textblobRanking
        self.textblobScore = textblobScore
        self.ownRanking = ownRanking
        self.ownScore = ownScore
