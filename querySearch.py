import tweepy

import sys
sys.path.append('modules')
import twitterConnect_mod
import sentification_mod as sentification

#query Twitter
api = twitterConnect_mod.api

max_tweets = 1
query = input("Query: ")

searched_tweets = []
for status in tweepy.Cursor(api.search, q=query).items(max_tweets):
    searched_tweets.append(status)

tweet = searched_tweets[0]
author = tweet.author.name
text = tweet.text
print("Name: " + author)
print("Tweet: " + text)

#extract sentiment
s = sentification.Sentifier('TextBlob')
print(s.sentiment(text))
print(s.subjectivity(text))
