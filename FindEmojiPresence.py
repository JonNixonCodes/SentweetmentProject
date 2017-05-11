# import all emojiis
import nltk
from nltk.tokenize import word_tokenize, RegexpTokenizer, TweetTokenizer, WhitespaceTokenizer

import  pickle
import emoji
from emoji import UNICODE_EMOJI, EMOJI_UNICODE


f = open('modules/jar_of_pickles/emoji_unicode.pickle', 'rb')
emoji_unicode = pickle.load(f)
f.close()

f = open('modules/jar_of_pickles/happy_emoji_unicode.pickle', 'rb')
happy_emoji_unicode = pickle.load(f)
f.close()

f = open('modules/jar_of_pickles/neutral_emoji_unicode.pickle', 'rb')
neutral_emoji_unicode = pickle.load(f)
f.close()

f = open('modules/jar_of_pickles/sad_emoji_unicode.pickle', 'rb')
sad_emoji_unicode = pickle.load(f)
f.close()

import csv
import datetime
import time
import sys
sys.path.append('modules')
import sentification_mod as sentification

def ProcessTweet(text, sentifier):
    sentiment = sentifier.sentiment(text)
    confidence = sentifier.confidence(text)
    return (sentiment, confidence)

# main
TIME_INTERVAL = datetime.timedelta(0, 5) #set time interval to 10 sec
#start_time = datetime.datetime.now()
start_time = datetime.datetime(2017, 5, 3, 7, 53, 28)
end_time = start_time + TIME_INTERVAL
interval_iter = 0
num_tweets = 0
pos_tweets = 0

f = open('graph_data.txt', 'w')
f.close()

s1 = sentification.Sentifier('NB')
csvFile = open('tweets.csv', 'r')
offset = 0

while(1):
    csvFile.seek(offset)
    csvReader = csv.DictReader(csvFile)
    for row in csvReader:
        author = row['author']
        date_created = datetime.datetime.strptime(row['date_created'], "%Y-%m-%d %H:%M:%S")
        text = row['text']
        
        if (date_created > end_time):
            # iterate interval
            interval_iter += 1
            # reset time interval
            start_time = end_time
            end_time = start_time + TIME_INTERVAL
            # reset counters
            num_tweets = 0
            pos_tweets = 0
            assert date_created < end_time
            
            print('\n\n########################################################')
            print('################ WROTE TO graph_data.txt  ################')
            print('########################################################\n\n')

        # presence of emoji
        text = emoji.demojize(text)
        # remove emoji
        regTokenizer = RegexpTokenizer('\s+', gaps=True)
        tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
        words = regTokenizer.tokenize(text)
        happy_emoji_count = 0
        sad_emoji_count = 0
        neutral_emoji_count = 0
        emoji_count = 0
        for w in words:
            if w in emoji_unicode.keys():
                if w in neutral_emoji_unicode.keys():
                    neutral_emoji_count += 1
                    text = text.replace(w, '__NEUTRAL_EMOJI__', 1)
                elif w in happy_emoji_unicode.keys():
                    happy_emoji_count += 1
                    text = text.replace(w, '__HAPPY_EMOJI__', 1)
                elif w in sad_emoji_unicode.keys():
                    sad_emoji_count += 1
                    text = text.replace(w, '__SAD_EMOJI__', 1)
                else:
                    emoji_count += 1
                    text = text.replace(w, '__EMOJI__')            
                    words = tokenizer.tokenize(text)
        # calculating sentiment and confidence
        sentiment, confidence = ProcessTweet(text, s1)
        # updating counters
        num_tweets += 1
        if sentiment == 'pos':
            pos_tweets += 1
        if (emoji_count != 0):
            # printing shit
            print('Author: ', author)
            print('Date Created: ', date_created)
            print('Text: ', text)        
            print('Sentiment: ', sentiment)
            print('Confidence: ', str(confidence))
            print('happy = ', happy_emoji_count)
            print('neutral = ', neutral_emoji_count)
            print('sad = ', sad_emoji_count, '\n')
            f = open('emoji_tweets.txt', 'a')            
            f.write(text)
            f.close()
    offset = csvFile.tell()
    # Wait for 1 second ... save processing power
    time.sleep(1)
csvFile.close()
