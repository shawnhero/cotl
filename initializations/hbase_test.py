# this script is to test the ttl function in hbase
import happybase
import time
from struct import *
connection = happybase.Connection('c0tl.com')
user_newsfeed = connection.table('user_newsfeed')
# row = user_newsfeed.row(pack('Q',1),columns=['newsfeed'])
# for key, data in user_newsfeed.scan(row_start=pack('Q',10), row_stop=pack('Q',15)):
# 	print unpack('Q',key), data

for key, data in user_newsfeed.scan(row_prefix="\xc2\n\xd4\xd7o\xe9wY\xaa'\xa0\xc9\x9b\xffg\x10"):
	print key, data