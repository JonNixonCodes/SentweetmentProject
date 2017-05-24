#!/usr/bin/env python
"""
Test file for creating data training module
"""
import sys
import random
import pickle
import numpy as np
import getFeatures
import train


def main():
    num_features = 4000
    """check arguments"""
    if len(sys.argv) > 1:
        num_features = int(sys.argv[1])
        print('arg1: num_features = {}'.format(num_features))
    
    """load test tweets"""
    print('importing test tweets...', end='')
    f = open('modules/jar_of_pickles/stanfordTestData.pickle', 'rb')
    test_tweets = pickle.load(f)
    f.close()
    print('DONE')

    """separate pos/neg tweets"""
    print('separating pos/neg tweets...', end='')
    pos_tweets = []
    neg_tweets = []
    ntl_tweets = []
    for tweet in test_tweets:
        if tweet[1] == 'pos':
            pos_tweets.append(tweet)
        elif tweet[1] == 'neg':
            neg_tweets.append(tweet)
        else:
            ntl_tweets.append(tweet)
    test_tweets = pos_tweets + neg_tweets
    random.shuffle(test_tweets)
    print('DONE')
    
    """obtain features from test tweets"""
    print('extracting features from test tweets...', end='')
    featureset_keys = train.import_featureset_keys(num_features)    
    num_tweets = len(test_tweets)
    blankfeatureset = (np.zeros(num_features, dtype=bool))
    testing_set = [(blankfeatureset, '...')]*num_tweets
    for index, tweet in enumerate(test_tweets):
        features = getFeatures.extract_featureset_array(tweet[0], featureset_keys)
        sentiment = tweet[1]
        testing_set[index] = (features, sentiment)
    print('DONE')

    """pickle testing set"""
    print('saving test featureset...', end='')
    f = open('modules/jar_of_pickles/stanfordTestFeaturesets.pickle', 'wb')
    pickle.dump(testing_set, f)
    f.close()
    print('DONE')
    
if __name__ == "__main__":
    main()
