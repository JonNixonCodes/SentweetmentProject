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
start_time = datetime.datetime(2017, 5, 2, 20, 45, 25)
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
            # update graph_data.txt
            f = open('graph_data.txt', 'a')
            sentval = int(pos_tweets/num_tweets*100)
            line = "{0}, {1}\n".format(interval_iter, sentval)
            f.write(line)
            f.close()
            # reset counters
            num_tweets = 0
            pos_tweets = 0
            assert date_created < end_time
            
            print('\n\n########################################################')
            print('################ WROTE TO graph_data.txt  ################')
            print('########################################################\n\n')

        # calculating sentiment and confidence
        sentiment, confidence = ProcessTweet(text, s1)
        # updating counters
        num_tweets += 1
        if sentiment == 'pos':
            pos_tweets += 1
        
        # printing shit
        print('Author: ', author)
        print('Date Created: ', date_created)
        print('Text: ', text)        
        print('Sentiment: ', sentiment)
        print('Confidence: ', str(confidence), '\n')
    offset = csvFile.tell()
    # Wait for 1 second ... save processing power
    time.sleep(1)
csvFile.close()
