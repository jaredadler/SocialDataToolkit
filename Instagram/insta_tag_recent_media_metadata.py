import time, re, sys
from instagram.client import InstagramAPI
from datetime import datetime
import cPickle as pickle
import unicodecsv as csv
from types import *

'''collects a set number (argument 3, max ~3000) of a tag's (argument 1)\
recent instagram media and dumps the metadata into a csv file (argument 2, no extension)\
'''

#authentication for instagram API
inapi = InstagramAPI(access_token="", client_secret="")

#directory for server
target_dir = ""

hashtag = sys.argv[1]
csv_filename = target_dir + str(sys.argv[2]) + "_" + str(datetime.now().day) + "_" + str(datetime.now().hour) + ".csv"
call_count = sys.argv[3]

#for an instagram user id, retrieves recent media and dumps metadata into a csv
def recent_media_metadata(tag, target_filename, count):
    f_dir = open(target_filename, 'wb')
    igcsv = csv.writer(f_dir, encoding = 'utf-8', quoting = csv.QUOTE_ALL)
    igcsv.writerow(['username', 'fullname', 'id', 'caption', 'likes', 'comments', 'time', 'link', 'lowres', 'standardres', 'thumbnail', 'userid'])
    total_calls = int(int(count) / 20)
    max_id_ = None
    for i in range(0, total_calls):
        print i
        time.sleep(20)
        m_list, next_url = inapi.tag_recent_media(20, max_id_, str(hashtag))
        for m in m_list:
            #catches photos lacking a caption which was throwing an error
            if type(m.caption) is NoneType:
                caption = ""
            else:
                caption = m.caption.text
            try:
                m_datalist = [m.user.username, m.user.full_name, m.id, caption, m.like_count, m.comment_count,\
                              m.created_time, m.link, m.images['low_resolution'].url, m.images['standard_resolution'].url,\
                              m.images['thumbnail'].url, m.user.id]
            except Exception, e:
                print e
                print "issue with this media:"
                print m
            #print m_datalist
            igcsv.writerow(m_datalist)
        #extracts max_id from next_url for next call
        match = re.search(r'\d+', next_url[::-1])
        backwards_code = match.group()
        max_id_ = backwards_code[::-1]


recent_media_metadata(hashtag, csv_filename, call_count)
