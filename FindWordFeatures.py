#File: FindWordFeatures.py
import nltk
from nltk.tokenize import word_tokenize, RegexpTokenizer, TweetTokenizer, WhitespaceTokenizer
from nltk.corpus import stopwords
import emoji
import pickle
import re

from textblob import TextBlob

# load word features
f = open('modules/jar_of_pickles/stanford_features6000.pickle', 'rb')
word_features = pickle.load(f)
f.close()


class Sentifier:
    classifier_dict = {'TextBlob' : 0, 'NB' : 1}    
    def __init__(self, classifier):
        # load all classifiers
        try:
            self.classifier = self.classifier_dict[classifier]
        except KeyError:
            print('invalid classifier')
        
    def sentiment(self, text):
        if self.classifier == self.classifier_dict['TextBlob']:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            if polarity > 0: return 'pos'
            elif polarity < 0: return 'neg'
            elif polarity == 0: return 'neutral'
            else:
                print('Error: invalid polarity')
    
        elif self.classifier == self.classifier_dict['NB']:
            features = find_features(text)
            return MNBclassifier.classify(features)
    def confidence(self, text):
        if self.classifier == self.classifier_dict['TextBlob']:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            if polarity < 0:
                polarity = -polarity
            return polarity
        elif self.classifier == self.classifier_dict['NB']:
            features = find_features(text)
            probDist = MNBclassifier.prob_classify(features)
            return probDist.prob(probDist.max())
            
        elif self.classifier == self.classifier_dict['NB']:
            features = find_features(text)
            return MNBclassifier.classify(features)
        

    def subjectivity(self, text):
        if self.classifier == self.classifier_dict['TextBlob']:
            blob = TextBlob(text)
            return blob.sentiment.subjectivity
# function to find features from text
def find_features(text, tokenizer):
    words = tokenizer.tokenize(text)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features
        
# main
tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
f = open('modules/jar_of_pickles/emoji_unicode.pickle', 'rb')
emoji_unicode = pickle.load(f)
f.close()
f = open('modules/jar_of_pickles/happy_emoji_unicode.pickle', 'rb')
happy_emoji_unicode = pickle.load(f)
f.close()
f = open('modules/jar_of_pickles/neutral_emoji_unicode.pickle', 'rb')
neutral_emoji_unicode = pickle.load(f)
f.close()
f = open('modules/jar_of_pickles/sad_emoji_unicode.pickle', 'rb')
sad_emoji_unicode = pickle.load(f)
f.close()

text = emoji.emojize("Python is so great :grinning_face: :grinning_face: :) :( :] :[ :\ :baby_light_skin_tone:")
text = emoji.demojize(text)
# remove emoji
regTokenizer = RegexpTokenizer('\s+', gaps=True)
words = regTokenizer.tokenize(text)
happy_emoji_count = 0
sad_emoji_count = 0
neutral_emoji_count = 0
for w in words:
    if w in emoji_unicode.keys():
        if w in neutral_emoji_unicode.keys():
            neutral_emoji_count += 1
            text = text.replace(w, '__NEUTRAL_EMOJI__', 1)
        elif w in happy_emoji_unicode.keys():
            happy_emoji_count += 1
            text = text.replace(w, '__HAPPY_EMOJI__', 1)
        elif w in sad_emoji_unicode.keys():
            sad_emoji_count += 1
            text = text.replace(w, '__SAD_EMOJI__', 1)
        else:
            text = text.replace(w, '__EMOJI__')            
words = tokenizer.tokenize(text)
print(text)
print(words)
print('happy = ', happy_emoji_count)
print('neutral = ', neutral_emoji_count)
print('sad = ', sad_emoji_count)
