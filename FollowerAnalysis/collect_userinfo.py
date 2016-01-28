import tweepy, time, csv, urllib2, calendar, sys, os.path
from datetime import datetime
from math import ceil
import cPickle as pickle
import numpy as np
import pandas as pd

"""
input:  a txt file with a list of twitter handles, maximum size 18000
	    name of txt file including extension should be first argument
output: a csv with the user info for each of the handles
	    additionally, pickles this userinfo in case the csv has issues
"""

auth = tweepy.OAuthHandler("", "") #put keys and secrets here
auth.set_access_token("", "")
api = tweepy.API(auth)

#creates n-sized chunks of a list
def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

"""
define filename of sns
requires extension
"""
ulistf = sys.argv[1]
ulistname = ulistf.split('.')[0]

ulist = open(ulistf, 'rb').read()
ulist = ulist.split('\n')
ulist = [i.lower() for i in ulist]

if len(ulist) < 100:
	userobjs = {}
	info = api.lookup_users(screen_names = ulist)
	for user in info:
		userobjs[str(user.screen_name.lower())] = user
elif len(ulist) < 18000:
	uchunks = list(chunks(ulist, 100))
	userobjs = {}
	for chunk in uchunks:
		infochunk = api.lookup_users(user_ids = chunk)
		for user in infochunk:
			userobjs[str(user.screen_name.lower())] = user
else:
	print "Error: User list is too long. Script must be modified to handle more than 18000 users."

pickle.dump(userobjs, open(ulistname + '_userobjs_' + datetime.now().strftime('%d-%H-%M') + '.p', 'wb'))

userdf = pd.DataFrame(ulist, columns = ['screenname'])

userdf['userid'] = userdf['screenname'].apply(lambda x: None if x not in ulist else userobjs[x].id_str)
userdf['statuses_count'] = userdf['screenname'].apply(lambda x: None if x not in ulist else np.int_(userobjs[x].statuses_count))
userdf['followers_count'] = userdf['screenname'].apply(lambda x: None if x not in ulist else np.int_(userobjs[x].followers_count))
userdf['friends_count'] = userdf['screenname'].apply(lambda x: None if x not in ulist else np.int_(userobjs[x].friends_count))
userdf['full_name'] = userdf['screenname'].apply(lambda x: None if x not in ulist else userobjs[x].name)
userdf['desc'] = userdf['screenname'].apply(lambda x: None if x not in ulist else userobjs[x].description.replace('\n', ' ').replace('\t', ' ').replace('\r', ' '))
userdf['location'] = userdf['screenname'].apply(lambda x: None if x not in ulist else userobjs[x].location)
userdf['creation_date'] = userdf['screenname'].apply(lambda x: None if x not in ulist else userobjs[x].created_at)
userdf['protected'] = userdf['screenname'].apply(lambda x: None if x not in ulist else userobjs[x].protected)
userdf['verified'] = userdf['screenname'].apply(lambda x: None if x not in ulist else userobjs[x].verified)

userdf.to_csv(ulistname + '_userinfo_' + datetime.now().strftime('%d-%H-%M')  + '.csv', encoding = 'utf-8', quoting = csv.QUOTE_ALL)
