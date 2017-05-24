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
    X_train = np.zeros((batch_size, num_features), dtype=bool)
    y_train = np.empty(batch_size, dtype='<U3')
    all_classes = np.array(('pos', 'neg'))    
    print('number of batches: {}\tbatch size: {}'.format(num_batches, batch_size))
    """opening file"""
    f = open('modules/jar_of_pickles/all_featuresets{}_{}.pickle'.format(num_features, num_tweets), 'rb')

    """import batch of featuresets"""        
    for batch_num in range(num_batches):            
        print('importing batch {}/{}...'.format(batch_num+1, num_batches), end='')
        batch = import_batch_featuresets(f)
        print('DONE')

        """partial training of classifier"""
        print('training on batch {}/{}...'.format(batch_num+1, num_batches), end='')
        for index, tweet in enumerate(batch):
            featureset = tweet[0]
            sentiment = tweet[1]
            X_train[index] = featureset
            y_train[index] = sentiment
        MNBclassifier.partial_fit(X_train, y_train, classes=all_classes)
        print('DONE')
        
    f.close()

    """save classifier"""
    print('saving classifier...', end='')    
    f = open('modules/jar_of_pickles/classifier_stanford{}_{}.pickle'.format(num_features, num_tweets), 'wb')
    pickle.dump(MNBclassifier, f)
    f.close()
    print('DONE')
        
    """testing"""
    testing_set = batch
    f.close()
    X = np.zeros((len(testing_set), num_features), dtype=bool)
    y = np.empty(len(testing_set), dtype='<U3')
    for index, tweet in enumerate(testing_set):
        featureset = tweet[0]
        sentiment = tweet[1]
        X[index] = featureset
        y[index] = sentiment    
    print('DONE')
    print('(DODGY) testing...', end='')
    accuracy = MNBclassifier.score(X, y)
    print('DONE')
    print('acc = {}'.format(accuracy))

if __name__ == "__main__":
    main()
