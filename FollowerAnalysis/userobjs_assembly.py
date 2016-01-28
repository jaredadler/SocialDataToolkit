import tweepy, time, csv, urllib2, calendar, sys, os.path, glob, random
from datetime import datetime
from math import ceil
import cPickle as pickle
import numpy as np
import pandas as pd

"""
2 inputs:
	- a folder full of pickled dictionaries from collect_userobjs.py (arg 1)
	- csv from compare_x_idlists.py with a column of userids and columns for each influencer (arg 2)
output:
	- ...
"""

pickle_directory = sys.argv[1] #directory where a folder full of pickled dictionaries from collect_userobjs.py are located
useridcsvDirectory = sys.argv[2] #csv

"""
picks up all files with the extension .p
iterates through the files, loads them, adds them to master dictionary allUserObjects
"""
allFiles = glob.glob(pickle_directory + '*.p')
allUserObjects = {}
for p in allFiles:
    UserObjectDict = pickle.load(open(p, 'rb'))
    allUserObjects.update(UserObjectDict)

"""
creates set for checking existence of id in keys of dictionary
this is needed for the lambda expressions to add attributes to the csv below
"""
allUserObjects_set = set(allUserObjects.keys())

"""
loads csv of all user ids and boolean overlap columns
creates set for checking existence of id
"""
ids_overlap = pd.read_csv(useridcsvDirectory, dtype = {'userid' : 'string'}, )
ids_overlap_set = set(list(ids_overlap['userid']))

"""
adds new columns to csv with additional user data
conditional statement is used to handle case where ids_overlap has an id not contained in allUserObjects
"""
ids_overlap['screenname'] = ids_overlap['userid'].apply(lambda x: None if x not in allUserObjects_set else allUserObjects[x].screen_name)
ids_overlap['statuses_count'] = ids_overlap['userid'].apply(lambda x: None if x not in allUserObjects_set else np.int_(allUserObjects[x].statuses_count))
ids_overlap['followers_count'] = ids_overlap['userid'].apply(lambda x: None if x not in allUserObjects_set else np.int_(allUserObjects[x].followers_count))
ids_overlap['friends_count'] = ids_overlap['userid'].apply(lambda x: None if x not in allUserObjects_set else np.int_(allUserObjects[x].friends_count))
ids_overlap['full_name'] = ids_overlap['userid'].apply(lambda x: None if x not in allUserObjects_set else allUserObjects[x].name)
ids_overlap['desc'] = ids_overlap['userid'].apply(lambda x: None if x not in allUserObjects_set else allUserObjects[x].description.replace('"', ' '))
ids_overlap['location'] = ids_overlap['userid'].apply(lambda x: None if x not in allUserObjects_set else allUserObjects[x].location)
ids_overlap['creation_date'] = ids_overlap['userid'].apply(lambda x: None if x not in allUserObjects_set else allUserObjects[x].created_at)
ids_overlap['protected'] = ids_overlap['userid'].apply(lambda x: None if x not in allUserObjects_set else allUserObjects[x].protected)
ids_overlap['verified'] = ids_overlap['userid'].apply(lambda x: None if x not in allUserObjects_set else allUserObjects[x].verified)
ids_overlap['handle_url'] = ids_overlap['userid'].apply(lambda x: None if x not in allUserObjects_set else 'http://twitter.com/' + allUserObjects[x].screen_name)
ids_overlap['coupons_deals'] = ids_overlap['userid'].apply(lambda x: None if x not in allUserObjects_set else ('coupon' in allUserObjects[x].description.lower()) or ('deal' in allUserObjects[x].description.lower()))
ids_overlap['timezone'] = ids_overlap['userid'].apply(lambda x: None if x not in allUserObjects_set else allUserObjects[x].time_zone)

"""
save output as csv with full quoting, though still worried quotes in desc will mess up csv
pickle output
"""
ids_overlap.to_csv(pickle_directory + 'assembled.csv', encoding='utf-8', index= False, quoting = csv.QUOTE_ALL)
pfile = open(pickle_directory + 'assembled.p', 'wb')
pickle.dump(ids_overlap, pfile)
pfile.close()