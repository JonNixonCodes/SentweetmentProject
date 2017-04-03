import sys
sys.path.append('modules')
import twitterConnect_mod

api = twitterConnect_mod.api

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print (tweet.text)

"""user = api.get_user('twitter')
print user.screen_name"""
