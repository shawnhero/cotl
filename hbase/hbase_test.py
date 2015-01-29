# this script is to test the ttl function in hbase
# in hbase_create.py, change line 56 to 
# 'newsfeed': dict(max_versions=1,time_to_live=10)
import happybase
import time
from struct import *
connection = happybase.Connection('ec2-54-67-86-242.us-west-1.compute.amazonaws.com')
user_newsfeed = connection.table('user_newsfeed')
user_newsfeed.put(
		'test', 
		{
			'newsfeed:testcol': pack('i', 1024)
		}
	)
count = 0
while True:
	row = user_newsfeed.row('test')
	print count, unpack('i',row['newsfeed:testcol'])  # prints 'value1'
	time.sleep(1)
	count = count+1

