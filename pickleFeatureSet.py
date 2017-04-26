# train NB classifier on tweets from Stanford corpus

import nltk
from nltk.tokenize import word_tokenize, RegexpTokenizer, TweetTokenizer
from nltk.corpus import stopwords
import random
import pickle
import re
import string
#from sklearn.naive_bayes import GaussianNB

f = open('modules/jar_of_pickles/stanford_features6000.pickle', 'rb')
word_features = pickle.load(f)
f.close()

tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
def find_features(text):
    words = tokenizer.tokenize(text)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features

f = open('modules/jar_of_pickles/stanford1600000.pickle', 'rb')
all_tweets = pickle.load(f)
f.close()

#get featuresets of pos and negative tweets
featuresets = []
pos_tweets = []
neg_tweets=[]
for t in all_tweets:
    if t[1] == 'pos':
        pos_tweets.append(t)
    elif t[1] == 'neg':
        neg_tweets.append(t)

N = 8000 #number of featuresets from each category
for (text, category) in pos_tweets[:N]:
    featuresets.append((find_features(text), category))
for (text, category) in neg_tweets[:N]:
    featuresets.append((find_features(text), category))
    
"""
for f in featuresets[:10]:
    for (key, value) in f[0].items():
        if value == True:
            print (key)
"""
# pickle feature sets
f = open('modules/jar_of_pickles/stanford_featuresets1600000.pickle', 'wb')
pickle.dump(featuresets, f)
f.close()

#classifier = GaussianNB()


"""
all_words = []
for t in all_tweets:
    tokenizer = RegexpTokenizer(r"\w+'?\w+")
    words = tokenizer.tokenize(t[0])
    for w in words:
        all_words.append(w.lower())

fdist = nltk.FreqDist(all_words)
#print 100 most common words
word_features = list(fdist.most_common())[:100] 
print(word_features)
"""
