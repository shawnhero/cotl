#!/usr/bin/env python

## consumer behavior for the topic 'post_photos'

import threading, logging, time, sys
import happybase
from struct import *
import json
from kafka import KafkaClient, SimpleConsumer, MultiProcessConsumer
from pyelasticsearch.client import ElasticSearch


_DEBUG_MODE = True
_HBASEHOST = 'c0tl.com'
_ESHOST = 'http://localhost:9200/'
#'ec2-54-67-86-242.us-west-1.compute.amazonaws.com'

# given a single parsed message, do the following
# 1. Find the nearest N neighbors from elastic search
# 2. Append that photo to their newsfeeds with a time-to-live(days) para
def consume_newsfeed(parsed_msg, hbasepool, eshost, indexname='geos', doc_name='user_geos',tbl_name='user_newsfeed', num_neighbors=10):
	lon = parsed_msg['data']['location']['longitude']
	lat = parsed_msg['data']['location']['latitude']
	# connect to elasticsearch and return the neighbors
	es = ElasticSearch(eshost)
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
	print "Query to elasticsearch,"
	print query
	res =  es.search(query, index=indexname, doc_type=doc_name)
	## store the nearest neighbors in a list
	uids = [int(r['_id']) for r in res['hits']['hits']]
	print len(uids), "neighbors Retrieved from ElasticSearch!"
	print "UIDs as following,\n", uids
	## connect the hbase
	# connection = happybase.Connection(hbasehost)
	with hbasepool.connection() as connection:
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
						# dump the json file of the photo infor
						'newsfeed:'+col_qualifier: json.dumps(parsed_msg['data'])
					}
				)
	if _DEBUG_MODE:
		# return the list of uids
		return uids
	else:
		return

# given a single parsed message, add the user-photo info to the user_photos table
def consume_userphotos(parsed_msg, hbasepool, tbl_name='user_photos'):
	# connection = happybase.Connection(hbasehost)
	with hbasepool.connection() as connection:
		# column qualifier is timestamp+photoID
		# 10 Byte + 8 Byte = 18 Byte, which is not too bad
		col_qualifier = str(parsed_msg['data']['photo']['timeposted']) + str(parsed_msg['data']['photo']['pid'])
		rowkey = pack('Q', parsed_msg['data']['user_id'])
		timeposted = int(parsed_msg['data']['photo']['timeposted'])
		## ready to write to hbase
		# connection = happybase.Connection(hbasehost)
		user_photos = connection.table(tbl_name)
		## the columnqualifier has enough information
		## for now the value is only
		user_photos.put(
				rowkey, 
					{'posted_photos:'+col_qualifier: "",
					}, timestamp=timeposted
				)
	if _DEBUG_MODE:
		return rowkey
	else:
		return


def unpack_photo(rawvalue):
	rawvalue['metrics:numLiked'] = unpack('i',rawvalue['metrics:numLiked'])[0]
	rawvalue['metrics:numViewed'] = unpack('i',rawvalue['metrics:numViewed'])[0]
	rawvalue['details:postby'] = unpack('Q',rawvalue['details:postby'])[0]
	rawvalue['details:born_lat'] = unpack('d',rawvalue['details:born_lat'])[0]
	rawvalue['details:born_lon'] = unpack('d',rawvalue['details:born_lon'])[0]
	rawvalue['details:timeposted'] = unpack('i',rawvalue['details:timeposted'])[0]

# given a single parsed message, add the photo info to photo table
def consume_photo(parsed_msg, hbasepool, tbl_name='photos'):
	try:
		# pack the user/photo id as unsigned long long, which takes 8 Bytes
		rowkey = pack('Q', int(parsed_msg['data']['photo']['pid']))
		postby = pack('Q', parsed_msg['data']['user_id'])
		born_lat = pack('d', parsed_msg['data']['location']['latitude'])
		born_lon = pack('d', parsed_msg['data']['location']['longitude'])
		tags = parsed_msg['data']['photo']['tags']
		# make sure the 'tags' is a list
		assert(type(tags)==type([]))
		# convert it to a comma-seperated string
		tags = ','.join(tags)
		# pack it
		title = parsed_msg['data']['photo']['title']
		description = parsed_msg['data']['photo']['description']
		url = parsed_msg['data']['photo']['URL']
		timeposted = int(parsed_msg['data']['photo']['timeposted'])
		## ready to write to hbase
		with hbasepool.connection() as connection:
			photos = connection.table(tbl_name)
			photos.put(	
					rowkey, 
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
	except Exception as e:
		print str(e)
		raise
# given a single parsed message, index the user's location as well as the photo's location in elastic search
def consume_location(parsed_msg, eshost, indexname='geos', user_type='user_geos', photo_type='photo_geos'):
	# establish a connection to ElasticSearch
	assert(parsed_msg['data']['action']=='post')
	es = ElasticSearch(eshost)
	user_doc = {
		'uid': int(parsed_msg['data']['user_id']),
		"location" : {
 			"lat" : parsed_msg['data']['location']['latitude'],
 			"lon" : parsed_msg['data']['location']['longitude']
 		}
	}
	photo_doc = {
		'pid': int(parsed_msg['data']['photo']['pid']),
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

class Consume(threading.Thread):
	def __init__(self, consumer,name,  eshost, hbasepool):
		threading.Thread.__init__(self)
		self.consumer = consumer
		self.name = name
		self.eshost = eshost
		self.hbasepool = hbasepool

	def run(self):
		for message in self.consumer:
			print '-'*100
			print self.name, 'pulls out one msg,'
			print '-'*100
			try:
				self.handle_msg(message.message.value)
			except Exception as e:
				print str(e)
				print message.message.value
				pass
	def handle_msg(self, msg):
		parsed_msg = json.loads(msg)
		if self.name=='newsfeed':
			consume_newsfeed(parsed_msg, self.hbasepool, self.eshost)
		elif self.name=='userphoto':
			consume_userphotos(parsed_msg, self.hbasepool)
		elif self.name=='photos':
			consume_photo(parsed_msg, self.hbasepool)
		elif self.name=='geoupdate':
			consume_location(parsed_msg, self.eshost)
		print self.name, 'Result Good'





if __name__ == "__main__":
	if len(sys.argv)!=3:
		print "Usage: [*.py] [topicname] [simple/multi]"
		sys.exit(0)
	kafka = KafkaClient("localhost:9092")
	post_topic_name = sys.argv[1]
	if sys.argv[2]=='simple':
		
		consumer_newsfeed = SimpleConsumer(kafka, "newsfeed", post_topic_name,iter_timeout=5)
		consumer_userphoto = SimpleConsumer(kafka, "userphoto", post_topic_name,iter_timeout=5)

		consumer_photos = SimpleConsumer(kafka, "photos", post_topic_name,iter_timeout=5)

		consumer_geoupdate = SimpleConsumer(kafka, "geoupdate", post_topic_name,iter_timeout=5)

	elif sys.argv[2]=='multi':
		# This will split the number of partitions among two processes
		consumer_newsfeed = MultiProcessConsumer(kafka, "newsfeed", post_topic_name, auto_commit=True,num_procs=1)
		consumer_userphoto = MultiProcessConsumer(kafka, "userphoto", post_topic_name, auto_commit=True,num_procs=1)
		consumer_photos = MultiProcessConsumer(kafka, "photos", post_topic_name, auto_commit=True,num_procs=1)
		consumer_geoupdate = MultiProcessConsumer(kafka, "geoupdate", post_topic_name, auto_commit=True,num_procs=1)
	else:
		print "Usage: [*.py] [topicname] [simple/multi]"
		sys.exit(0)
	pool = happybase.ConnectionPool(size=6, host=_HBASEHOST)
	threads = [ Consume(consumer_newsfeed, 'newsfeed', _ESHOST,pool),
				Consume(consumer_userphoto, 'userphoto', _ESHOST,pool),
				Consume(consumer_photos, 'photos', _ESHOST,pool),
				Consume(consumer_geoupdate, 'geoupdate', _ESHOST,pool)
				]
	for t in threads:
		t.start()