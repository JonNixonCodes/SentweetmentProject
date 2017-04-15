import pickle

f = open('modules/jar_of_pickles/stanford1600000.pickle', 'rb')
all_tweets = pickle.load(f)
f.close()

print(all_tweets[0])
print(all_tweets[1])

pos = 0
neg = 0
neutral = 0
for t in all_tweets:
    if t[1] == 'pos':
        pos += 1
    elif t[1] == 'neg':
        neg += 1
    elif t[1] == 'neutral':
        neutral += 1
print('positive: ' + str(pos))
print('negative: ' + str(neg))
print('neutral: ' + str(neutral))
