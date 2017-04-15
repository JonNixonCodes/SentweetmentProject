import csv
import pickle

csvfile = open('corpora/stanford/training.1600000.processed.noemoticon.csv', newline = '', encoding='ISO-8859-1')
reader = csv.reader(csvfile, delimiter = ',', quotechar = '"')

all_tweets = []

for row in reader:
    if row[0] == '0':
        polarity = 'neg'
    elif row[0] == '2':
        polarity = 'neutral'        
    elif row[0] == '4':
        polarity = 'pos'
    all_tweets.append((row[5], polarity))

save_all_tweets = open('modules/jar_of_pickles/stanford1600000.pickle', 'wb')
pickle.dump(all_tweets, save_all_tweets)
save_all_tweets.close()
