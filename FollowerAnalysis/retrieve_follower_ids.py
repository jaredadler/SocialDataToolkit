import tweepy, time, csv, urllib2, calendar, sys
from datetime import datetime
from math import ceil
import networkx as nx
import cPickle as pickle

auth = tweepy.OAuthHandler("", "")
auth.set_access_token("", "")
api = tweepy.API(auth, retry_count = 2, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

handle_source = sys.argv[1]

#gets the ids of all of the user's followers
def retrieve_follower_ids(user_handle):
	follower_cursors = tweepy.Cursor(api.followers_ids, screen_name = user_handle)
	allf = []
	counter = 0
	for follower_cursor in follower_cursors.items():
		counter = counter + 1
		if counter%75000 == 0:
			time.sleep(900)
		try:
			print follower_cursor
			allf.append(str(follower_cursor))
		except tweepy.TweepError:
			time.sleep(30)
			allf.append(str(follower_cursor))
	#write the ids to a file
	f = open(user_handle + '_followers_ids.txt', 'w')
	for user in allf:
		f.write(user)
		f.write('\n')
	f.close()
	#return allf

retrieve_follower_ids(handle_source)