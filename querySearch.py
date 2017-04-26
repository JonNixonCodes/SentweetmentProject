import tweepy

import sys
sys.path.append('modules')
import twitterConnect_mod
import sentification_mod as sentification

def process_tweet(tweet, sentifier):
    author = tweet.author.name
    text = tweet.text
    favourited = tweet.favorited
    retweeted = tweet.retweeted
    language = tweet.lang
    sentiment = sentifier.sentiment(text)
    #print("Name: " + author)
    print("Tweet: " + text)
    print("Sentiment:" + sentiment)
    #print("Language: " + language)
    #print("Retweeted:" + str(retweeted))
    #print("Favourited:" + str(favourited))
    
def process_page(page, sentifier):
    print("Number of tweets: " + str(len(page)))
    for tweet in page:
        if tweet.lang == 'en':
            process_tweet(tweet, sentifier)

s1 = sentification.Sentifier('TextBlob')
s2 = sentification.Sentifier('NB')

#query Twitter
api = twitterConnect_mod.api

max_tweets = 1
query = input("Query: ")

searched_pages = []
for page in tweepy.Cursor(api.search, q=query).pages(1):
    searched_pages.append(page)

page = searched_pages[0]
process_page(page, s2)
