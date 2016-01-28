import tweepy, time, csv, urllib2, calendar, sys, os.path, itertools, collections
from datetime import datetime
from math import ceil
import cPickle as pickle
import numpy as np
import pandas as pd

"""
input:  a pickled dictionary from collect_tweetobjs.py
output: a csv of tweets with metadata for sorting to look at top retweets and other things
		a csv of top hashtags and group hashtag usage
"""

pickledtweetobjs = sys.argv[1]

tweetobjs = pickle.load(open(pickledtweetobjs, 'rb'))

allTweetIDs = [i for i in tweetobjs.values()]
allTweetIDs = {k: v for d in allTweetIDs for k, v in d.items() }

"""
create dataframe with useful attributes from the tweetobjs
"""
tweetdf = pd.DataFrame(allTweetIDs.keys(), columns = ['tweetid'])
tweetdf['Text'] = tweetdf['tweetid'].apply(lambda x: None if x not in allTweetIDs else allTweetIDs[x].text.replace('\n', ' ').replace('\t', ' ').replace('\r', ' '))
tweetdf['Author'] = tweetdf['tweetid'].apply(lambda x: None if x not in allTweetIDs else allTweetIDs[x].author.screen_name)
tweetdf['Favorites Count'] = tweetdf['tweetid'].apply(lambda x: None if x not in allTweetIDs else allTweetIDs[x].favorite_count)
tweetdf['Retweet Count'] = tweetdf['tweetid'].apply(lambda x: None if x not in allTweetIDs else allTweetIDs[x].retweet_count)
tweetdf['url'] = tweetdf['tweetid'].apply(lambda x: None if x not in allTweetIDs else allTweetIDs[x].source_url)
tweetdf['Is Retweet'] = tweetdf['tweetid'].apply(lambda x: True if (allTweetIDs[x].text[:2] == "RT") else False)
tweetdf['tweeturl'] = tweetdf['tweetid'].apply(lambda x: "http://twitter.com/" + allTweetIDs[x].author.screen_name + "/status/" + x)
tweetdf['Hashtags'] = tweetdf['tweetid'].apply(lambda x: None if x not in allTweetIDs else [i['text'].lower() for i in allTweetIDs[x].entities['hashtags']])
tweetdf['Links'] = tweetdf['tweetid'].apply(lambda x: None if x not in allTweetIDs else [i['expanded_url'] for i in allTweetIDs[x].entities['urls']])
tweetdf['User Mentions'] = tweetdf['tweetid'].apply(lambda x: None if x not in allTweetIDs else [tuple([i['id_str'], i['screen_name']]) for i in allTweetIDs[x].entities['user_mentions']])
tweetdf['source'] = tweetdf['tweetid'].apply(lambda x: None if x not in allTweetIDs else allTweetIDs[x].source)

tweetdf.to_csv(pickledtweetobjs.split('.')[0] + '.csv', encoding = 'utf-8', quoting = csv.QUOTE_ALL)

"""
tallies up all hashtags, provides count
"""
allhashtags = list(itertools.chain(*list(tweetdf['Hashtags'])))
alltagcount = collections.Counter(allhashtags).most_common(100)

with open(pickledtweetobjs.split('.')[0] +'_toptags.csv','wb') as out:
    csv_out = csv.writer(out)
    csv_out.writerow( [ 'hashtag' , 'count' ] )
    for row in alltagcount:
        csv_out.writerow(row)

"""
tallies up proportion of group using hashtags
"""
hashtagsunique = []
for user in tweetobjs.keys():
	usertagset = list(set(itertools.chain(*list(tweetdf[tweetdf['Author'] == user]['Hashtags']))))
	hashtagsunique = hashtagsunique + usertagset
uniqtagcount = collections.Counter(hashtagsunique).most_common(100)

with open(pickledtweetobjs.split('.')[0] +'_toptagsproportion.csv','wb') as out2:
    csv_out = csv.writer(out2)
    csv_out.writerow( [ 'hashtag' , 'proportion' ] )
    for row in uniqtagcount:
        csv_out.writerow([row[0], (float(row[1]) / len(tweetobjs.keys()))])
