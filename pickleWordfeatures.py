# train NB classifier on tweets from Stanford corpus

import nltk
from nltk.tokenize import word_tokenize, RegexpTokenizer, TweetTokenizer
from nltk.corpus import stopwords
import random
import pickle
import string

f = open('modules/jar_of_pickles/stanford1600000.pickle', 'rb')
all_tweets = pickle.load(f)
f.close()

#split tweets into positive and negative
pos_tweets = []
neg_tweets = []
for t in all_tweets:
    if t[1] == 'pos':
        pos_tweets.append(t)
    elif t[1] == 'neg':
        neg_tweets.append(t)

#print(pos_tweets[0])
#print(neg_tweets[0])
#print(stopwords.words('english'))
_stopwords = stopwords.words('english')

tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
all_words = []
for t in all_tweets:
    #downcase, remove handles, reduce repeated character sequencese to length 3
    words = tokenizer.tokenize(t[0])
    for w in words:
        w = w.lower()
        if w not in _stopwords:
            if w not in string.punctuation: #removes some punctuation
                all_words.append(w)

word_features = []
fdist = nltk.FreqDist(all_words)
#print 100 most common words
most_common = fdist.most_common(6000)
for i in most_common:
    word_features.append(i[0])
print(word_features)

#pickle word features
f = open('modules/jar_of_pickles/stanford_features6000.pickle', 'wb')
pickle.dump(word_features, f)
f.close()

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
