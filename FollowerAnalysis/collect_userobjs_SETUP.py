import cPickle as pickle

"""
creates necessary files to start running collect_userobjs.py
only run this once before starting a new collection
"""
#empty list for checked_directory
l = []
pickle.dump(l, open('checked_ids.p', 'wb'))

#txt file for the errorlog
with open('errorlog.txt', 'wb') as elfile:
	elfile.write('x')

#switch txt file for using two API keys
with open('switch.txt', 'wb') as swfile:
	swfile.write('on')
