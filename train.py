#!/usr/bin/env python
"""
Test file for creating data training module
"""
import sys
import pickle
import string
import random
import re
import nltk
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


def import_featuresets(num_features, num_tweets):
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
            print(len(all_featuresets))
        except EOFError:
            return all_featuresets
    
    
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

    """check arguments"""
    if len(sys.argv) > 1:
        num_features = int(sys.argv[1])
        print('arg1: num_features = {}'.format(num_features))
    if len(sys.argv) > 2:
        num_tweets = int(sys.argv[2])
        print('arg2: num_tweets = {}'.format(num_tweets))        

    """import featuresets from subset of tweets"""
    print('importing featuresets...', end='')
    all_featuresets = import_featuresets(num_features, num_tweets)
    print('DONE')
    print(len(all_featuresets))
        
    """separate pos/neg tweets"""
    print('separating pos/neg featuresets...', end='')
    for tweet in all_featuresets:
        if tweet[1] == 'pos':
            pos_tweets.append(tweet)
        elif tweet[1] == 'neg':
            neg_tweets.append(tweet)
    print('DONE')

    """allocate training set"""
    print('allocating training set...', end='')    
    random.shuffle(pos_tweets)
    random.shuffle(neg_tweets)
    training_size = int(num_tweets*0.9)
    training_featuresets = pos_tweets[:int(training_size/2)] + neg_tweets[:int(training_size/2)]
    random.shuffle(training_featuresets)
    print('DONE')
    #print(len(training_featuresets))    

    """allocate testing set"""
    print('allocating testing set...', end='')
    testing_size = num_tweets-training_size
    testing_featuresets = pos_tweets[-int(testing_size/2):] + neg_tweets[-int(testing_size/2):]
    print('DONE')
    #print(len(testing_featuresets))
    
    """training"""
    print('training classifier...', end='')
    MNBclassifier = SklearnClassifier(MultinomialNB())
    MNBclassifier.train(training_featuresets)
    print('DONE')
    #print(sorted(MNBclassifier.labels()))    

    """testing"""
    #s1 = "I'm happy in the morning :)"
    #result = MNBclassifier.classify(extract_features(s1, featureset))
    #print(result)
    accuracy = nltk.classify.accuracy(MNBclassifier, testing_featuresets)
    print('acc = {}'.format(accuracy))

    """save classifier"""
    print('saving classifier...', end='')    
    f = open('modules/jar_of_pickles/classifierStanford{}.pickle'.format(training_size), 'wb')
    pickle.dump(MNBclassifier, f)
    f.close()
    print('DONE')

if __name__ == "__main__":
    main()
