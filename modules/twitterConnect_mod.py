#file: twitterConnect_mod.py
import tweepy

consumer_key = 'Mooa8lXLBw64M5zgI3YZOPOCM'
consumer_secret =  'ZwG1ySZFoMecK32FOYolv0Mua0O7WrrxldTmjJWxHmk7NLhl72'
access_token =  '742573307153637377-eaMd96n7D4Bk2nyPzYlEPYaSE7fO5Ou'
access_token_secret = 'wwNFjex0nNuab6GFqCTKLNtm605p9ZsATTd7M4KSWrxhg'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# below are useful variables required by scripts which import this module
api = tweepy.API(auth)
