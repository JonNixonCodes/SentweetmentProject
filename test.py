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
    
    
def main():
    """check arguments"""
    if len(sys.argv) > 1:
        num_features = int(sys.argv[1])
        print('arg1: num_features = {}'.format(num_features))
    if len(sys.argv) > 2:
        num_tweets = int(sys.argv[2])
        print('arg2: num_tweets = {}'.format(num_tweets))        

    """load trained classifiers"""
    f = open('modules/jar_of_pickles/classifier_stanford6000_10000.pickle', 'rb')
    stanfordMNBclassifier = pickle.load(f)
    f.close
        
    """load test sets"""
    print('importing testset...', end='')
    f = open('modules/jar_of_pickles/testset_stanford{}.pickle'.format(num_features), 'rb')
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

    """testing"""
    print('testing...', end='')
    accuracy = stanfordMNBclassifier.score(X, y)
    print('DONE')
    print('acc = {}'.format(accuracy))

if __name__ == "__main__":
    main()
