import tweepy
import dataset
db = dataset.connect("sqlite:///tweets.db")

import sys
sys.path.append('modules')
import twitterConnect_mod
import sentification_mod as sentification

def filter_tweet(tweet):
    language = tweet.lang
    if language != 'en':
        return False
    return True
    

def process_tweet(tweet, sentifier):
    author = tweet.author.name
    text = tweet.text
    date_created = tweet.created_at
    favourited = tweet.favorited
    retweeted = tweet.retweeted
    language = tweet.lang
    sentiment = sentifier.sentiment(text)
    confidence = sentifier.confidence(text)
    #print("Name: " + author)
    print("Tweet: " + text)
    print(date_created)
    print("Sentiment:" + sentiment)
    print(confidence)    
    #print("Language: " + language)
    #print("Retweeted:" + str(retweeted))
    #print("Favourited:" + str(favourited))
    return sentiment

class MyStreamListener(tweepy.StreamListener):
    i = 0
    buffer_count = 0
    pos_count = 0
    neg_count = 0
    s2 = sentification.Sentifier('NB')
    def on_status(self, status):
        if status.lang == 'en':
            if self.buffer_count == 10:
                f = open('graph_data.txt', 'a')
                sentval = int((self.pos_count - self.neg_count)*10)
                line = "{0}, {1}\n".format(self.i, sentval)
                f.write(line)
                f.close()
                self.i += 1
                self.buffer_count = 0
                self.pos_count = 0
                self.neg_count = 0
            sentiment = process_tweet(status, self.s2)
            self.buffer_count += 1
            if sentiment == 'pos':
                self.pos_count += 1
            elif sentiment == 'neg':
                self.neg_count += 1
    #disconnect after receiving error 420
    def on_error(self, status_code):
        if status_code == 420:
            #returning false on an on_data disconnects the stream
            return False

#query Twitter
api = twitterConnect_mod.api
#initialise graph_data
f = open('graph_data.txt', 'w')
f.close()
query = input('Enter your query: ')
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=MyStreamListener())
myStream.filter(track=[query])
