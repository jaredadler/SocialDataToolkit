#Social Data Toolkit

---

##For Instagram

### Hashtags

`insta_tag_recent_media_metadata.py` collects a specified number of recent instagram media that included a specified hashtag in the caption or comments.

##For Twitter

### Additional metadata for social listening tools

For an exported CSV of social media posts from Radian6 or Netbase, `enhance_radian.py` and `enhance_netbase.py` add additional metadata (retweet count, favorite count, user's time zone, etc.) for any included tweets.

### User(s) tweet history

For a list of twitter handles, 

- `collect_tweetobjs.py` bulk-collects the last 1000 tweets.
- `tweet_trends.py` structures the output from `collect_tweetobjs.py` as a csv and counts top hashtags used by the users in the list.

### A user's list of followers

Originally designed to make analyzing the followers of one or more Twitter users with more than 100k followers easier.

- `retrieve_follower_ids.py` collects all of a Twitter user's followers' user IDs and saves them as a txt file.
- `compare_x_idlists.py` takes multiple follower lists from `retrieve_follower_ids.py` and assesses follower overlap.
- `collect_userobjs.py` takes the follower overlap comparison table from `compare_x_idlists.py` and collects the user object (containing handle, follower count, profile description, etc.) for each user ID (requires `collect_userobjs_SETUP.py` to be run once first). This is designed to be scheduled to run every 8 minutes until all user objects are collected (in which the output will just be empty pickles).
- `userobjs_assembly.py` structures the user objects in the output of `collect_userobjs.py` as a csv for further analysis of the users(s) followers.

More simply, `collect_userinfo.py` collects the user objects from a list of Twitter handles and structures their content as a CSV.