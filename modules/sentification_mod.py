#File: sentification_mod.py

import nltk
import textblob
import pickle

from textblob import TextBlob

class Sentifier:
    classifier_dict = {'TextBlob' : 0, 'NB' : 1}    
    def __init__(self, classifier):
        # load all classifiers
        try:
            self.classifier = self.classifier_dict[classifier]
        except KeyError:
            print('invalid classifier')
        
    def sentiment(self, text):
        if self.classifier == self.classifier_dict['TextBlob']:
            blob = TextBlob(text)
            return blob.sentiment.polarity            

    def confidence(self, text):
        pass

    def subjectivity(self, text):
        if self.classifier == self.classifier_dict['TextBlob']:
            blob = TextBlob(text)
            return blob.sentiment.subjectivity
