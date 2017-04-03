#File: sentiment_mod.py

import nltk
import random
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize

class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf

documents_f = open("jar_of_pickles/documents.pickle", "rb")
documents = pickle.load(documents_f)
documents_f.close()

word_features2k_f = open("jar_of_pickles/word_features2k.pickle", "rb")
word_features = pickle.load(word_features2k_f)
word_features2k_f.close()

def find_features(document):
    tokens = word_tokenize(document)
    words = []
    for w in tokens:
        words.append(w.lower())
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features



featuresets_f = open("jar_of_pickles/featuresets.pickle", "rb")
featuresets = pickle.load(featuresets_f)
featuresets_f.close()

random.shuffle(featuresets)
#print(len(featuresets))

testing_set = featuresets[10000:]
training_set = featuresets[:10000]



open_file = open("jar_of_pickles/originalNaiveBayes2k.pickle", "rb")
classifier = pickle.load(open_file)
open_file.close()


open_file = open("jar_of_pickles/MNB_classifier2k.pickle", "rb")
MNB_classifier = pickle.load(open_file)
open_file.close()


open_file = open("jar_of_pickles/BernoulliNB_classifier2k.pickle", "rb")
BernoulliNB_classifier = pickle.load(open_file)
open_file.close()


open_file = open("jar_of_pickles/LogisticRegression_classifier2k.pickle", "rb")
LogisticRegression_classifier = pickle.load(open_file)
open_file.close()


open_file = open("jar_of_pickles/LinearSVC_classifier2k.pickle", "rb")
LinearSVC_classifier = pickle.load(open_file)
open_file.close()


open_file = open("jar_of_pickles/SGD_classifier2k.pickle", "rb")
SGD_classifier = pickle.load(open_file)
open_file.close()




voted_classifier = VoteClassifier(
                                  classifier,
                                  LinearSVC_classifier,
                                  MNB_classifier,
                                  BernoulliNB_classifier,
                                  LogisticRegression_classifier)




def sentiment(text):
    feats = find_features(text)
    return voted_classifier.classify(feats), voted_classifier.confidence(feats)

def feature_count(text):
    feats = find_features(text)
    count = 0
    for key in feats:
        if feats[key] == True:
            count += 1
    return count
