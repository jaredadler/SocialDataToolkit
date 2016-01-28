import pandas as pd
import numpy as np
import tweepy, csv, sys

"""
Takes a XLSX of social media posts exported from Netbase and adds more metadata for all of the posts that came from Twitter.
Input - a XLSX exported from Netbase
Output - a new CSV with additional columns for:
	- Number of Retweets
	- Number of Favorites
	- Whether the post is a retweet
	- Hashtags used in the post
	- Links included in the post
	- @-mentions included in the post (if the post is a retweet, the screenname of the being retweeted is included)
	- App or other manner that the tweet was posted
	- Profile description of the Twitter account
	- T/F of the user's verification status
	- Time zone of the user (useful for determining where the user is located)
	- Author's location


How to use:
From the command line, run the script with one additional argument: the CSV export, including the extension, like this:
python enhance_netbase.py netbaseexport.xlsx
"""

"""
required inputs
"""

#including extension, the name of the csv exported from radian
netbase_export = sys.argv[1]
#four-line txt with four twitter auth api keys
#could convert this to an argument if it's easier
twitterapikey = ''

#twitter API key import and authorization
twauth = open(twitterapikey, 'rb').read()
twauth = twauth.split('\n')

auth = tweepy.OAuthHandler(twauth[0], twauth[1])
auth.set_access_token(twauth[2], twauth[3])
api = tweepy.API(auth, retry_count = 2, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

"""
required functions
"""
def chunks(l, n):
    #Yield successive n-sized chunks from l.
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def is_retweet(x):
    #checks to see if a post is a retweet by looking at the first two characters
    if x not in tweetobjs:
        return None
    elif tweetobjs[x].text[:2] == "RT":
        return True
    else:
        return False

"""
opens netbase export XLSX as pandas df
from url column, extracts tweetid into a list in a new column
skips rows that aren't tweets
"""
df = pd.read_excel(netbase_export)
df[df['Domain'] == 'twitter.com']
df['TWEETID'] = df.apply(lambda x: np.nan if (x['Domain'] != 'twitter.com')\
                         else str(x['URL'].split('/')[-1:][0]), axis = 1)

"""
all tweetids, as a list, are chunked into groups of 100
tweet objects are pulled 100 at a time using tweepy method statuses_lookup
tweet objects structured in dictionary tweetobjs for later reference
"""
tweetobjs = {}
twidchunks = chunks(list(df['TWEETID'].dropna()), 100)
for chunk in twidchunks:
    tweetinfo = api.statuses_lookup(chunk, include_entities = True)
    for tweet in tweetinfo:
        tweetobjs[tweet.id_str] = tweet

"""
set of expressions to add new columns to the netbase export XLSX
if a row is not from twitter or if the twitter API did not retrieve a tweet object for a specific tweet, all new columns are left blank
"""
df['Favorites Count'] = df['TWEETID'].apply(lambda x: None if x not in tweetobjs else tweetobjs[x].favorite_count)
df['Retweet Count'] = df['TWEETID'].apply(lambda x: None if x not in tweetobjs else tweetobjs[x].retweet_count)
df['Is Retweet'] = df['TWEETID'].apply(is_retweet)
df['Hashtags'] = df['TWEETID'].apply(lambda x: None if x not in tweetobjs else [i['text'] for i in tweetobjs[x].entities['hashtags']])
df['Links'] = df['TWEETID'].apply(lambda x: None if x not in tweetobjs else [i['expanded_url'] for i in tweetobjs[x].entities['urls']])
df['User Mentions'] = df['TWEETID'].apply(lambda x: None if x not in tweetobjs else [tuple([i['id_str'], i['screen_name']]) for i in tweetobjs[x].entities['user_mentions']])
df['source'] = df['TWEETID'].apply(lambda x: None if x not in tweetobjs else tweetobjs[x].source)
df['Desc of Author'] = df['TWEETID'].apply(lambda x: None if x not in tweetobjs else tweetobjs[x].author.description)
df['Author is Verified'] = df['TWEETID'].apply(lambda x: None if x not in tweetobjs else tweetobjs[x].author.verified)
df['Author Time Zone'] = df['TWEETID'].apply(lambda x: None if x not in tweetobjs else tweetobjs[x].author.time_zone)
df['Author Location'] = df['TWEETID'].apply(lambda x: None if x not in tweetobjs else tweetobjs[x].author.location)

"""
saves an updated csv with the added metadata
"""
df.to_csv(netbase_export.replace('.xlsx', '') + '_enhanced.csv', encoding = 'utf-8', quoting = csv.QUOTE_ALL)
