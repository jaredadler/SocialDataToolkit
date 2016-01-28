import tweepy, time, csv, urllib2, calendar, sys, os.path, glob, itertools
from datetime import datetime
from math import ceil
import cPickle as pickle
import numpy as np
import pandas as pd

"""
input: a folder full of text files that have twitter userids, ideally from retrieve_follower_ids.py (argument 1)
output: a csv with a column for the userids and boolean columns to show which txt file (follower set) the id occurs in (argument 2)
"""

#directory where userid lists (txts) are located
uid_folder = sys.argv[1]
#list of userid list titles (in most cases, will be twitter influencer screennames. same input as collect_userinfo.py)
list_titles = sys.argv[2]
#export filename
export_fname = sys.argv[3]

#corresponds to retrieve_follower_ids.py
#takes lists of userids in a specified directory txtfile_directory,
#creates a dict, KEY is user screenname cross-referenced from list of users, VALUE is set
#of userids
def collect_userid_txts(txtfile_directory, userid_list):
    #open userid list
    uidlist = open(userid_list, 'rb').read()
    uidlist = uidlist.split('\n')
    allFiles = glob.glob(txtfile_directory + '*.txt')
    #concatenate all txt in the folder
    m = pd.DataFrame()
    idlists = {}
    for files in allFiles:
        idlist = open(files, 'rb').read()
        idlist = idlist.split('\n')
        del idlist[-1]
        for user in uidlist:
            if user.lower() in files.lower():
                idlists[user] = set(idlist)
            else:
                pass
    return idlists

#input is dictionary
#output is df of all ids (set of all dict values) and boolean columns for each key
def userid_df(userid_dict):
	idset = set(list(itertools.chain(*[i[1] for i in userid_dict.iteritems()])))
	df = pd.DataFrame(list(idset))
	df['userid'] = df[0]
	del df[0]
	for i in userid_dict:
		df[i] = df['userid'].apply(lambda x: x in userid_dict[i])
	return df

fulldf = userid_df(collect_userid_txts(uid_folder, list_titles))
fulldf.to_csv(export_fname + '.csv', index = False, quoting = csv.QUOTE_ALL)
