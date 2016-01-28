import tweepy, time, csv, calendar, sys, os.path
from datetime import datetime
import cPickle as pickle
import numpy as np
import pandas as pd

"""
input:  a txt file with a list of twitter screennames, maximum size 18000
	    name of txt file, including extension should be first argument
output: a pickled dictionary of the last 1000 tweets (or less if user has fewer than 1000) of each user in input
"""

auth = tweepy.OAuthHandler("", "") #put your keys and secrets here
auth.set_access_token("", "")
api = tweepy.API(auth, retry_count = 2, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

"""
define filename of sns
requires extension
"""
ulistf = sys.argv[1]
ulistname = ulistf.split('.')[0]

ulist = open(ulistf, 'rb').read()
ulist = ulist.split('\n')
ulist = [i.lower() for i in ulist]

sns_tweet_obj = {}
for user in ulist:
    print str(ulist.index(user) + 1) + " out of " + str(len(ulist))
    time.sleep(13)
    user_tweetobj = {}
    try:
        for i in range(0,10,1):
            tweets = api.user_timeline(user, count = 100, page = i, include_entities = True)
            for tweet in tweets:
                user_tweetobj[str(tweet.id_str)] = tweet
            sns_tweet_obj[user] = user_tweetobj
            time.sleep(5)
    except tweepy.error.TweepError or tweepy.TweepError, e:
        print "some kind of error because %s" % e
        time.sleep(13)
        continue

pickle.dump(sns_tweet_obj, open(ulistname + '_tweetobjs' + datetime.now().strftime('%d-%H-%M')  + '.p', 'wb'))