#!/usr/bin/env python
"""
Test trained models on labelled data
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
from sklearn.metrics import f1_score
    
    
def main():
    num_features = 1000
    num_tweets = 10000
    """check arguments"""
    if len(sys.argv) > 1:
        num_features = int(sys.argv[1])
        print('arg1: num_features = {}'.format(num_features))
    if len(sys.argv) > 2:
        num_tweets = int(sys.argv[2])
        print('arg2: num_tweets = {}'.format(num_tweets))        

    """load trained classifiers"""
    f = open('modules/jar_of_pickles/classifier_stanford{}_{}.pickle'.format(num_features, num_tweets), 'rb')
    stanfordMNBclassifier = pickle.load(f)
    f.close
        
    """load test sets"""
    tests = []
    print('importing testset (stanford)...', end='')
    f = open('modules/jar_of_pickles/testset_stanford{}.pickle'.format(num_features), 'rb')
    tests.append((pickle.load(f), 'stanford'))
    f.close()
    print('DONE')

    print('importing testset (STS)...', end='')
    f = open('modules/jar_of_pickles/testset_STS{}.pickle'.format(num_features), 'rb')
    tests.append((pickle.load(f), 'STS'))
    f.close()
    print('DONE')

    print('importing testset (nltk)...', end='')
    f = open('modules/jar_of_pickles/testset_nltk{}.pickle'.format(num_features), 'rb')
    tests.append((pickle.load(f), 'nltk'))
    f.close()
    print('DONE')
    
    """testing"""
    all_classes= np.array(('pos', 'neg'))        
    for t in tests:
        print('testing ({})...'.format(t[1]), end='')
        testing_set = t[0]
        X_test = np.zeros((len(testing_set), num_features), dtype=bool)
        y_test = np.empty(len(testing_set), dtype='<U3')
        for index, tweet in enumerate(testing_set):
            featureset = tweet[0]
            sentiment = tweet[1]
            X_test[index] = featureset
            y_test[index] = sentiment    
        accuracy = stanfordMNBclassifier.score(X_test, y_test)
        y_pred = stanfordMNBclassifier.predict(X_test)
        fscore = f1_score(y_test, y_pred, labels=all_classes, average=None)
        print('DONE')
        print('acc = {}'.format(accuracy))
        print('f-measure = {}'.format(fscore))

if __name__ == "__main__":
    main()
