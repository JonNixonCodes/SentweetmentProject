import tweepy
import csv

import sys
sys.path.append('modules')
import twitterConnect_mod
import sentification_mod as sentification


class MyStreamListener(tweepy.StreamListener):
    BUF_SIZE = 100
    buf_count = 0
    buf = []

    def filter_tweet(self, tweet):
        if tweet.lang != 'en':
            return False
        return True

    def flush_buf(self):
        csvFile = open('tweets.csv', 'a')
        fieldnames = ['author', 'text', 'date_created', 'favourited', 'retweeted']
        csvWriter = csv.DictWriter(csvFile, fieldnames=fieldnames)
        for tweet in self.buf:
            csvWriter.writerow(tweet)
        csvFile.close()
        self.buf = []
        
        print('\n####################################')
        print('######## WROTE TO tweet.csv ########')
        print('####################################\n')
        
    def process_tweet(self, tweet):
        new = dict(author = tweet.author.name,
             text = tweet.text,
             date_created = tweet.created_at,
             favourited = tweet.favorited,
             retweeted = tweet.retweeted)
        print('Date Created: ' + str(new['date_created']))
        print(new['text'])
        self.buf.append(new)
    
    def on_status(self, status):
        if self.filter_tweet(status) != True:
            return
        self.process_tweet(status)
        self.buf_count += 1
        if self.buf_count == self.BUF_SIZE:
            self.flush_buf()
            self.buf_count = 0
            
    #disconnect after receiving error 420
    def on_error(self, status_code):
        if status_code == 420:
            #returning false on an on_data disconnects the stream
            return False

#query Twitter
api = twitterConnect_mod.api
query = input('Enter your query: ')

# clear CSV file and write header
csvFile = open('tweets.csv', 'w')
fieldnames = ['author', 'text', 'date_created', 'favourited', 'retweeted']
csvWriter = csv.DictWriter(csvFile, fieldnames=fieldnames)
csvWriter.writeheader()
csvFile.close()

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=MyStreamListener())
myStream.filter(track=[query])
