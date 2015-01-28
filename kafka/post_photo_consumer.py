 #!/usr/bin/env python
## consume the message from kafka

## 1. Send the 'user post photo' event/other relations to HBase
## 2. Send the 'user is at location' infor to Solr
## 3. Retrieve nearyby users and add the photo to their newsfeed 
## 6. Send the actual photo to S3

# to do, figure out how to do batch job of a single consumer

import threading, logging, time
import happybase
from struct import *
import json
from kafka import KafkaClient, MultiProcessConsumer
from pyelasticsearch.client import ElasticSearch

#'ec2-54-67-86-242.us-west-1.compute.amazonaws.com'

# given a single parsed message, do the following
# 1. Find the nearest N neighbors from elastic search
# 2. Append that photo to their newsfeeds with a time-to-live(days) para
def consume_newsfeed(parsed_msg, hbasehost, eshost, indexname='geos', doc_name='user_geos',tbl_name='user_newsfeed', num_neighbors=10, ttl=3):
	lon = parsed_msg['data']['location']['longitude']
	lat = parsed_msg['data']['location']['latitude']
	# connect to elasticsearch and return the neighbors
	es = ElasticSearch()
	query = {
		"from" : 0, "size" : num_neighbors,
		'query': {
			 "match_all" : { }
		 }
		 ,
		 "sort" : [
			{
				"_geo_distance" : {
					"location" : [lat, lon],
					"order" : "asc",
					"unit" : "km"
				}
			}
		]

	 }
	res =  es.search(query, index=indexname, doc_type=doc_name)
	## store the nearest neighbors in a list
	uids = [r['_source']['uid'] for r in res['hits']['hits']]
	## connect the hbase
	connection = happybase.Connection(hbasehost)
	user_newsfeed = connection.table('user_newsfeed')
	## iterate the uids and update their newsfeed
	timeposted = int(parsed_msg['data']['photo']['timeposted'])
	pid = parsed_msg['data']['photo']['pid']
	for uid in uids:
		rowkey = pack('Q', uid)
		col_qualifier = str(timeposted)+str(pid)
		user_newsfeed.put(
				rowkey, 
				{
					'newsfeed:'+col_qualifier: pack('c', 0)
				}
			)

# given a single parsed message, add the user-photo info to the user_photos table
def consume_userphotos(parsed_msg, hbasehost, tbl_name='user_photos'):
	connection = happybase.Connection(hbasehost)
	user_photos = connection.table(tbl_name)
	# column qualifier is timestamp+photoID
	# 10 Byte + 8 Byte = 18 Byte, which is not too bad
	col_qualifier = str(parsed_msg['data']['photo']['timeposted']) + str(parsed_msg['data']['photo']['pid'])
	rowkey = pack('Q', parsed_msg['data']['user_id'])
	timeposted = int(parsed_msg['data']['photo']['timeposted'])
	## ready to write to hbase
	connection = happybase.Connection(hbasehost)
	user_photos = connection.table(tbl_name)
	## the columnqualifier has enough information
	## for now the value is only
	user_photos.put
			(	rowkey, 
				{	'posted_photos:'+col_qualifier: pack('c',0),
				}, timestamp=pack('i',timeposted)
			)



# given a single parsed message, add the photo info to photo table
def consume_photo(parsed_msg, hbasehost, tbl_name='photos'):
	# pack the user/photo id as unsigned long long, which takes 8 Bytes
	rowkey = pack('Q', parsed_msg['data']['photo']['pid'])
	postby = pack('Q', parsed_msg['data']['user_id'])
	born_lat = pack('d', parsed_msg['data']['location']['latitude'])
	born_lon = pack('d', parsed_msg['data']['location']['longitude'])
	tags = parsed_msg['data']['photo']['tags']
	# make sure the 'tags' is a list
	assert(type(tags)==type([]))
	# convert it to a comma-seperated string
	tags = ','.join(tags)
	# pack it
	tags = pack('s', tags)
	title = pack('s', parsed_msg['data']['photo']['title'])
	description = pack('s', parsed_msg['data']['photo']['description'])
	url = pack('s', parsed_msg['data']['photo']['URL'])
	timeposted = int(parsed_msg['data']['photo']['timeposted'])
	## ready to write to hbase
	connection = happybase.Connection(hbasehost)
	photos = connection.table(tbl_name)
	photos.put
			(	rowkey, 
				{	'metrics:numLiked': pack('i',0),
					'metrics:numViewed': pack('i',0),
					'details:postby': postby,
					'details:born_lat': born_lat,
					'details:born_lon': born_lon,
					'details:tags': tags,
					'details:title': title,
					'details:description': description,
					'details:url': url,
					'details:timeposted': pack('i', timeposted)
				}, timestamp=timeposted
			)

# given a single parsed message, index the user's location as well as the photo's location in elastic search
def consume_location(parsed_msg, eshost, indexname='geos', user_type='user_geos', photo_type='photo_geos'):
	# establish a connection to ElasticSearch
	assert(parsed_msg['data']['action']=='post')
	es = ElasticSearch()
	user_doc = 
	{
		'uid': parsed_msg['data']['user_id'],
		"location" : {
 			"lat" : parsed_msg['data']['location']['latitude'],
 			"lon" : parsed_msg['data']['location']['longitude']
 		}
	}
	photo_doc = 
	{
		'pid': parsed_msg['data']['photo']['pid'],
		"location" : {
 			"lat" : parsed_msg['data']['location']['latitude'],
 			"lon" : parsed_msg['data']['location']['longitude']
 		}
	}
	es.index(indexname, user_type, user_doc)
	es.index(indexname, photo_type, photo_doc)


	
	

# given a single parsed message
# store the message in rdd for batch jobs
# to do: important
def consume_activity_to_rdd(parsed_msg):
	pass


if __name__ == "__main__":
	client = KafkaClient("localhost:9092")
	post_topic_name = "posts"
	# This will split the number of partitions among two processes
	consumer_newsfeed = MultiProcessConsumer(kafka, "newsfeed", post_topic_name, auto_commit=True,num_procs=1)
	consumer_userphoto = MultiProcessConsumer(kafka, "userphoto", post_topic_name, auto_commit=True,num_procs=1)
	consumer_photos = MultiProcessConsumer(kafka, "photos", post_topic_name, auto_commit=True,num_procs=1)
	consumer_geoupdate = MultiProcessConsumer(kafka, "geoupdate", post_topic_name, auto_commit=True,num_procs=1)

	count = 0
	
	for message in consumer:
		print(message.message.value)

	# daemon = Consumer('consumer.pid')
	# if len(sys.argv) == 2:
	# 	if 'start' == sys.argv[1]:
	# 		daemon.start()
	# 	elif 'stop' == sys.argv[1]:
	# 		daemon.stop()
	# 	elif 'restart' == sys.argv[1]:
	# 		daemon.restart()
	# 	else:
	# 		print "Unknown command"
	# 		sys.exit(2)
	# 	sys.exit(0)
	# else:
	# 	print "usage: %s start|stop|restart" % sys.argv[0]
	# 	sys.exit(2)