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
    pos_tweets = []
    neg_tweets = []
    all_features = import_all_features
    num_features = 6000
    featureset_template = import_featureset_template(num_features)

    """separate pos/neg tweets"""
    for tweet in all_tweets:
        if tweet[1] == 'pos':
            pos_tweets.append(tweet)
        elif tweet[1] == 'neg':
            neg_tweets.append(tweet)

    """allocate training set"""
    random.shuffle(pos_tweets)
    random.shuffle(neg_tweets)
    training_size = 10000
    training_set = pos_tweets[:int(training_size/2)] + neg_tweets[:int(training_size/2)]
    random.shuffle(training_set)
    training_featuresets = []
    for tweet in training_set:
        text = tweet[0]
        sentiment = tweet[1]
        featureset = extract_featureset(text, featureset_template)
        training_featuresets.append((featureset, sentiment))

    """allocate testing set"""
    testing_size = 1000
    testing_set = pos_tweets[:-int(testing_size/2)] + neg_tweets[:-int(testing_size/2)]
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

    """save classifier"""
    f = open('modules/jar_of_pickles/classifierStanford{}.pickle'.format(training_size), 'wb')
    pickle.dump(MNBclassifier, f)
    f.close()

if __name__ == "__main__":
    main()
