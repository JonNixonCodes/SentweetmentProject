import tweepy

import sys
sys.path.append('modules')
import twitterConnect_mod

def process_tweet(tweet):
    author = tweet.author.name
    text = tweet.text
    date_created = tweet.created_at
    favourited = tweet.favorited
    retweeted = tweet.retweeted
    language = tweet.lang
    #print("Name: " + author)
    print("Tweet: " + text)
    print(date_created)
    #print("Language: " + language)
    #print("Retweeted:" + str(retweeted))
    #print("Favourited:" + str(favourited))

class MyStreamListener(tweepy.StreamListener):
    i = 0
    buffer_count = 0
    pos_count = 0
    neg_count = 0
    def on_status(self, status):
        process_tweet(status)
    #disconnect after receiving error 420
    def on_error(self, status_code):
        if status_code == 420:
            #returning false on an on_data disconnects the stream
            return False

# list all emojiis
emojis = []
for x in range(0x1F600, 0x1F647):
    print(chr(x).encode())
        
# main
api = twitterConnect_mod.api
UserMe = api.me()
print("id: " + UserMe.id_str)
print("name: " + UserMe.name)
print("screen name: " + UserMe.screen_name)
print("number of Tweets: " + str(UserMe.statuses_count))

# get a load of these DMs
dm_list = api.direct_messages()
for dm in dm_list:
    print("sender id: " + str(dm.sender_id))
    print("screen name: " + dm.sender_screen_name)
    print("text: " + dm.text)
    print("UTF-8 decoded: " + ':'.join(hex(ord(c)) for c in dm.text))

