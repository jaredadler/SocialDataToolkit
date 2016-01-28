import tweepy, time, csv, urllib2, calendar, sys, os.path
from datetime import datetime
from math import ceil
import cPickle as pickle
import numpy as np
import pandas as pd


"""
define directory location of csv and pickled dict
easier to set up to run on server
"""

target_directory = '' #working directory where all the files are
csv_directory = '' #with extension, csv with a column of userids named 'userid', ideally the output from compare_x_idlists.py
checked_directory = 'checked_ids.p' #with extension, an empty list pickled, this will fill up every time script runs
error_log = 'errorlog.txt' #with extension, a txt file where errors can be written to
switch_directory = 'switch.txt' #with extension, a txt file with "on" written in it. used to cycle API keys

"""
open the error log
"""
errorlog = open(target_directory + error_log, 'rb').read()
errorlog = errorlog.split('\n')

"""
this alternates the api authorizations used to query the api so it can be run twice as many times per hour
"""
switch = open(target_directory + switch_directory, 'rb').read()  
if switch == 'on':
	auth = tweepy.OAuthHandler("", "")
	auth.set_access_token("", "")
	f = open(target_directory + switch_directory, 'wb')
	f.write('off')
	f.close()
else:
	auth = tweepy.OAuthHandler("", "")
	auth.set_access_token("", "")
	f = open(target_directory + switch_directory, 'wb')
	f.write('on')
	f.close()
api = tweepy.API(auth)


#creates n-sized chunks of a list
def chunker(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

"""
open csv of ids
open pickled list of checked userids
define empty dictionary to dump this round of checked userids into
"""
ids = pd.read_csv(target_directory + csv_directory, dtype = {'userid' : 'string'})
checked = pickle.load(open(target_directory + checked_directory, 'rb'))
checked_set = set(checked)
userobjs = {}

"""
list of ids whose objects haven't been collected and dumped in the dict userobjs yet
breaks that list into chunks of 100 for twitter api call
"""
not_collected = [i for i in ids['userid'] if i not in checked_set]
chunks = list(chunker(not_collected, 100))

"""
queries twitter api with 100 userids at a time
adds each retrieved userobject to dictionary

only 180 chunks at a time due to rate limits
"""
for chunk in chunks[:180]:
	time.sleep(1)
	try:
		userinfo = api.lookup_users(user_ids = chunk)
		for x in userinfo:
			print x.screen_name
			checked.append(str(x.id_str))
			userobjs[str(x.id_str)] = x
	except tweepy.error.TweepError or tweepy.TweepError, e:
		print "Some kind of error with " + " because %s" % e
		errorlog.append(str(e))
		for i in chunk:
			checked.append(str(i))
			errorlog.append(str(i))

"""
pickle the updated dictionary
pickle the list of checked ids
"""
errorlog_f = open(target_directory + error_log, 'wb')
for i in errorlog:
	errorlog_f.write(i)
	errorlog_f.write('\n')
errorlog_f.close()
pickle.dump(checked, open(target_directory + checked_directory, 'wb'))
pickle.dump(userobjs, open(target_directory + datetime.now().strftime('%d-%H-%M') + 'userobjs.p', 'wb'))
			