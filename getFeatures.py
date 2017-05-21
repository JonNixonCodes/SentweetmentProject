#!/usr/bin/env python
"""
Test file for creating data training module
"""
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
    """Extract features from text and return formatted feature set"""
    featureset = featureset_template.copy()
    features = preprocess(text)
    for f in features:
        if f in featureset.keys():
            featureset[f] = True
    return featureset

    
def main():
    all_tweets = import_tweets()
    all_features = import_all_features()
    featureset_template = {}
    num_tweets = len(all_tweets)
    num_features = 6000

    fdist1 = FreqDist(all_features)
    print(fdist1.most_common(50))
    
    """define feature set"""
    for item in fdist1.most_common(num_features):
        featureset_template[item[0]] = False

    """save feature set template"""
    f = open('modules/jar_of_pickles/featureset{}.pickle'.format(num_features), 'wb')
    pickle.dump(featureset_template, f)
    f.close()

if __name__ == "__main__":
    main()
