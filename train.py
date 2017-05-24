#!/usr/bin/env python
"""
Test file for creating data training module
"""
import sys
import pickle
import string
import random
import re
import math
import nltk
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


def import_featureset_template(num_features):
    """Import and return featureset template with number of features"""
    try:
        f = open('modules/jar_of_pickles/featureset{}.pickle'.format(num_features), 'rb')
        featureset_template = pickle.load(f)
        f.close()
        return featureset_template
    except:
        print('Error: Loading file featureset{}'.format(num_features))
        return False


def import_featureset_keys(num_features):
    """Import and return featureset keys with number of features"""
    try:
        f = open('modules/jar_of_pickles/featureset_keys{}.pickle'.format(num_features), 'rb')
        featureset_keys = pickle.load(f)
        f.close()
        return featureset_keys
    except:
        print('Error: Loading file featureset_keys{}'.format(num_features))
        return False
    

def import_all_featuresets(num_features, num_tweets):
    """Import and return featuresets from subset of tweets"""
    all_featuresets = []
    try:
            f = open('modules/jar_of_pickles/all_featuresets{}_{}.pickle'.format(num_features, num_tweets), 'rb')
    except:
        print('Error: Loading file all_featureset{}_{}.pickle'.format(num_features, num_tweets))
        return False
    while True:
        try:
            all_featuresets = all_featuresets + pickle.load(f)
            #print(len(all_featuresets))
        except EOFError:
            return all_featuresets
    

def import_batch_featuresets(f):
    """import and return subset of featuresets from file"""
    try:
        batch = pickle.load(f)
        return batch
    except EOFError:
        return False

        
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
    """Extract features from text and return formatted feature set"""
    featureset = featureset_template.copy()
    features = preprocess(text)
    for f in features:
        if f in featureset.keys():
            featureset[f] = True
    return featureset

    
def main():
    pos_tweets = []
    neg_tweets = []
    num_features = 3000
    num_tweets = 10000
    MNBclassifier = MultinomialNB()

    """check arguments"""
    if len(sys.argv) > 1:
        num_features = int(sys.argv[1])
        print('arg1: num_features = {}'.format(num_features))
    if len(sys.argv) > 2:
        num_tweets = int(sys.argv[2])
        print('arg2: num_tweets = {}'.format(num_tweets))        

    """split training into batch processes"""
    batch_size = 5000
    num_batches = math.ceil(num_tweets/batch_size)
    print('number of batches: {}\tbatch size: {}'.format(num_batches, batch_size))
    if num_tweets > batch_size:
        """opening file"""
        f = open('modules/jar_of_pickles/all_featuresets{}_{}.pickle'.format(num_features, num_tweets), 'rb')

        """import batch of featuresets"""        
        for batch_num in range(num_batches):            
            print('importing batch {}/{}...'.format(batch_num+1, num_batches), end='')
            batch = import_batch_featuresets(f)
            print('DONE')

            """partial training of classifier"""
            print('training on batch {}/{}...'.format(batch_num+1, num_batches), end='')
            X = np.zeros((batch_size, num_features), dtype=bool)
            y = np.empty(batch_size, dtype='<U3')
            classes = np.array(('pos', 'neg'))
            for index, tweet in enumerate(batch):
                featureset = tweet[0]
                sentiment = tweet[1]
                X[index] = featureset
                y[index] = sentiment
            MNBclassifier.partial_fit(X, y, classes)
            print('DONE')
            #print(np.shape(X))
            #print(np.shape(y))            
        f.close()
        
    else:        
        """import featuresets from subset of tweets"""
        print('importing all featuresets...', end='')
        all_featuresets = import_all_featuresets(num_features, num_tweets)
        print('DONE')
        print(len(all_featuresets))
    
        """training"""        
        print('training classifier...', end='')
        X = np.zeros((num_tweets, num_features), dtype=bool)
        y = np.empty(num_tweets, dtype='<U3')
        for index, tweet in enumerate(all_featuresets):
            featureset = tweet[0]
            sentiment = tweet[1]
            X[index] = featureset
            y[index] = sentiment
        MNBclassifier.fit(X, y)
        print('DONE')

    """save classifier"""
    print('saving classifier...', end='')    
    f = open('modules/jar_of_pickles/classifierStanford{}_{}.pickle'.format(num_features, num_tweets), 'wb')
    pickle.dump(MNBclassifier, f)
    f.close()
    print('DONE')
        
    """testing"""
    print('importing testset...', end='')
    f = open('modules/jar_of_pickles/stanfordTestFeaturesets.pickle', 'rb')
    testing_set = pickle.load(f)
    f.close()
    X = np.zeros((len(testing_set), num_features), dtype=bool)
    y = np.empty(len(testing_set), dtype='<U3')
    for index, tweet in enumerate(testing_set):
        featureset = tweet[0]
        sentiment = tweet[1]
        X[index] = featureset
        y[index] = sentiment    
    print('DONE')
    print('testing...', end='')
    accuracy = MNBclassifier.score(X, y)
    print('DONE')
    print('acc = {}'.format(accuracy))

if __name__ == "__main__":
    main()
