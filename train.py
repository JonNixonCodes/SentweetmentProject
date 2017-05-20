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
    f = open('modules/jar_of_pickles/stanford1600000.pickle', 'rb')
    all_tweets = pickle.load(f)
    f.close()
    return all_tweets


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
    all_features = []
    featureset_template = {}
    for tweet in all_tweets[:1600]:
        features = preprocess(tweet[0])
        for f in features:
            all_features.append(f)
    fdist1 = FreqDist(all_features)
    #print(fdist1.most_common(50))
    
    """define feature set"""
    for item in fdist1.most_common(1000):
        featureset_template[item[0]] = False

    s1 = "This is just great I'm so happy!"
    #print(extract_features(s1, word_features))

    """allocate training set"""
    random.shuffle(all_tweets)
    training_set = all_tweets[:1000]
    training_featuresets = []
    for tweet in training_set:
        text = tweet[0]
        sentiment = tweet[1]
        featureset = extract_featureset(text, featureset_template)
        training_featuresets.append((featureset, sentiment))

    """allocate testing set"""
    n = len(all_tweets)
    testing_set = all_tweets[(n-1000):]
    testing_featuresets = []
    for tweet in testing_set:
        text = tweet[0]
        sentiment = tweet[1]
        featureset = extract_featureset(text, featureset_template)
        testing_featuresets.append((featureset, sentiment))
    #print(testing_feature_set[0])
    #print(training_feature_set[0])
    
    """training"""
    MNBclassifier = SklearnClassifier(MultinomialNB())
    MNBclassifier.train(training_featuresets)
    print(sorted(MNBclassifier.labels()))

    """testing"""
    #s1 = "I'm happy in the morning :)"
    #result = MNBclassifier.classify(extract_features(s1, featureset))
    #print(result)
    accuracy = nltk.classify.accuracy(MNBclassifier, testing_featuresets)
    print(accuracy)
    
    

if __name__ == "__main__":
    main()
