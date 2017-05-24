#!/usr/bin/env python
"""
Test file for creating data training module
"""
import sys
import os.path
import pickle
import string
import random
import re
import nltk
import math
import numpy as np
from nltk import FreqDist
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB

def import_tweets():
    """Import tweets from stanford corpora and return in all_tweets"""
    f = open('modules/jar_of_pickles/stanfordCorpora.pickle', 'rb')
    all_tweets = pickle.load(f)
    f.close()
    return all_tweets


def import_all_features():
    """Import and return  all features from all tweets in stanford corpora"""
    f = open('modules/jar_of_pickles/all_features1600000.pickle', 'rb')
    all_features = pickle.load(f)
    f.close()
    return all_features


def pickle_all_features():
    """Save all features from all tweets as all_features1600000.pickle"""
    all_tweets = import_tweets()
    num_tweets = len(all_tweets)
    for tweet in all_tweets:
        features = preprocess(tweet[0])
        for f in features:
            all_features.append(f)
    """save all_features"""
    f = open('modules/jar_of_pickles/all_features{}.pickle'.format(num_tweets), 'wb')
    pickle.dump(all_features, f)
    f.close()


def split_camelcase(text):
    """split camelCase into list"""
    return re.sub('(?!^)([A-Z][a-z]+)', r' \1', text).split()
    

def preprocess(text):
    """Pre-process text and return list of unigram, bigram, hashtag features
    reduce length, lower case, strip handles, remove stopwords"""
    tker = TweetTokenizer(reduce_len=True, strip_handles=True)
    stop_words = stopwords.words('english') + list(string.punctuation)    
    tokens = tker.tokenize(text)
    unigrams = []
    bigrams = []
    hashtags = []
    for t in tokens:
        if t.startswith('#'):
            hashtags.append(tuple(t))
            words = split_camelcase(t.replace('#', ''))
            for w in words:
                unigrams.append(w.lower())
        elif t not in stop_words:
            unigrams.append(t.lower())
    for wordpair in list(nltk.bigrams(unigrams)):
        bigrams.append(' '.join(wordpair))
    features = unigrams + bigrams
    return nltk.pos_tag(features) + hashtags


def extract_featureset(text, featureset_template):
    """Extract features from text and return feature set formatted as dict"""
    featureset = featureset_template.copy()
    features = preprocess(text)
    for f in features:
        if f in featureset.keys():
            featureset[f] = True
    return featureset


def extract_featureset_array(text, featureset_keys_sorted):
    """Extract features from text and return feature set formatted as numpy array"""
    features = preprocess(text)
    featureset = np.zeros(len(featureset_keys_sorted), dtype=bool)
    for f in features:
        if f in featureset_keys_sorted:
            key_index = featureset_keys_sorted.index(f)
            featureset[key_index] = True
    return featureset

    
def main():
    all_tweets = import_tweets()
    all_features = import_all_features()
    all_featuresets = []
    featureset_template = {}
    num_tweets = 10000
    num_features = 3000

    """check arguments"""
    if len(sys.argv) > 1:
        num_features = int(sys.argv[1])
        print('arg1: num_features = {}'.format(num_features))
    if len(sys.argv) > 2:
        num_tweets = int(sys.argv[2])
        print('arg2: num_tweets = {}'.format(num_tweets))                
    
    """define feature set"""
    print('generating featureset template...', end='')
    fdist1 = FreqDist(all_features)
    #print(fdist1.most_common(50))    
    for item in fdist1.most_common(num_features):
        featureset_template[item[0]] = False
    featureset_keys_sorted = sorted(featureset_template.keys())
    print('DONE')
        
    """save feature set keys"""
    print('saving featureset keys...', end='')
    f = open('modules/jar_of_pickles/featureset_keys{}.pickle'.format(num_features), 'wb')
    pickle.dump(featureset_keys_sorted, f)
    f.close()
    print('DONE')

    """separate pos/neg tweets"""
    print('separating pos/neg tweets...', end='')
    pos_tweets = []
    neg_tweets = []    
    for tweet in all_tweets:
        if tweet[1] == 'pos':
            pos_tweets.append(tweet)
        elif tweet[1] == 'neg':
            neg_tweets.append(tweet)
    print('DONE')

    """allocate set of tweets"""
    print('allocating {} tweets...'.format(num_tweets), end='')
    random.shuffle(pos_tweets)
    random.shuffle(neg_tweets)
    tweetset = pos_tweets[:int(num_tweets/2)] + neg_tweets[:int(num_tweets/2)]
    random.shuffle(tweetset)
    print('DONE')

    """split feature extraction into batch processes"""
    batch_size = 5000
    num_batches = math.ceil(num_tweets/batch_size)
    print('number of batches: {}\tbatch size: {}'.format(num_batches, batch_size))
    if num_tweets > batch_size:
        """write to file"""
        f = open('modules/jar_of_pickles/all_featuresets{}_{}.pickle'.format(num_features, num_tweets), 'wb')
        f.close()        
        for batch_num in range(num_batches):
            start = batch_num*batch_size
            end = start+batch_size-1
            if end > num_tweets: end = num_tweets-1
            batch = tweetset[start:end]

            """extract feature sets from batch of tweets"""
            print('extracting featuresets from batch {}/{}...'.format(batch_num+1, num_batches), end='')
            blankfeatureset = (np.zeros(len(featureset_keys_sorted), dtype=bool))
            batch_featuresets = [(blankfeatureset, '...')]*batch_size
            for index, tweet in enumerate(batch):
                featureset = extract_featureset_array(tweet[0], featureset_keys_sorted)
                sentiment = tweet[1]
                batch_featuresets[index] = ((featureset, sentiment))

            """save feature sets from batch of tweets"""
            print('saving...', end='')
            f = open('modules/jar_of_pickles/all_featuresets{}_{}.pickle'.format(num_features, num_tweets), 'a+b')
            pickle.dump(batch_featuresets, f)
            f.close()
            print('DONE')
            
    else: 
        """extracting feature sets from all tweets"""
        print('extracting featuresets from tweets...', end='')
        blankfeatureset = (np.zeros(len(featureset_keys_sorted), dtype=bool))
        all_featuresets = [(blankfeatureset, '...')]*num_tweets    
        for index, tweet in enumerate(tweetset):
            featureset = extract_featureset_array(tweet[0], featureset_keys_sorted)
            sentiment = tweet[1]
            all_featuresets[index] = ((featureset, sentiment))
            print('DONE')

        """save all feature sets from all tweets"""
        print('saving all featuresets...', end='')
        f = open('modules/jar_of_pickles/all_featuresets{}_{}.pickle'.format(num_features, num_tweets), 'wb')
        pickle.dump(all_featuresets, f)
        f.close()
        print('DONE')

if __name__ == "__main__":
    main()
