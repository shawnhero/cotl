# this script is to test the ttl function in hbase
# in hbase_create.py, change line 56 to 
# 'newsfeed': dict(max_versions=1,time_to_live=10)
import happybase
import time
from struct import *
connection = happybase.Connection('c0tl.com')
user_newsfeed = connection.table('user_newsfeed')
row = user_newsfeed.row(pack('Q',1),columns=['newsfeed'])
print row
