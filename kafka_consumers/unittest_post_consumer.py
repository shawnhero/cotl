import random
import unittest
from post_photo_consumer import *
from struct import *

# run unit tests for all the consumer workers
class TestConsumerWorkers(unittest.TestCase):

	def setUp(self):
		self.parsed_msg = {"data": {"action": "post", "photo": {"timeposted": 1422466662, "description": "", "tags": [], "URL": "https://farm8.staticflickr.com/7324/16388566132_ba5bbfd888_b.jpg", "title": "", "pid": 16388566132}, "user_id": 12, "location": {"latitude": 37.419809522865279, "longitude": -122.31275946636089}}}
		self.hbasehost = 'ec2-54-67-86-242.us-west-1.compute.amazonaws.com'
		self.eshost = 'http://localhost:9200/'

	def test_consume_newsfeed(self):
		print '-'*50
		print 'Testing newsfeed consumer..'
		print '-'*50
		# make sure the 10 neighbors 
		uids = consume_newsfeed(self.parsed_msg, self.hbasehost, self.eshost,num_neighbors=10)
		self.assertEqual(len(uids), 10)
		# make sure the 10 user has the newfeed with the photo
		connection = happybase.Connection(self.hbasehost)
		user_newsfeed = connection.table('user_newsfeed')
		for uid in uids:
			row = user_newsfeed.row(pack('Q',uid),columns=['newsfeed'])
			print "newsfeed of", uid
			for key in row.keys():
				print key[19:]
		print "Note, message pid is", self.parsed_msg['data']['photo']['pid']
		

	def test_consume_userphotos(self):
		print '-'*50
		print 'Testing user_photos consumer..'
		print '-'*50
		rowkey = consume_userphotos(self.parsed_msg, self.hbasehost)
		# make sure the user-photo relation is written to hbase
		connection = happybase.Connection(self.hbasehost)
		user_photos = connection.table('user_photos')
		row = user_photos.row(rowkey)
		print row

	def test_consume_photo(self):
		print '-'*10
		consume_photo(self.parsed_msg, self.hbasehost)
		connection = happybase.Connection(self.hbasehost)
		photos = connection.table('photos')
		rowkey = pack('Q', int(self.parsed_msg['data']['photo']['pid']))
		row = photos.row(rowkey)
		unpack_photo(row)
		print row

	def test_consume_location(self):
		print '-'*50
		print 'Testing location consumer..'
		print '-'*50
		consume_location(self.parsed_msg, self.eshost)
		# make sure the documents are correctly documented
		es = ElasticSearch(self.eshost)
		# query = {'from':0,'size':10,'query':{'match_all':{}}}
		res =  es.search('uid:12', index='geos', doc_type='user_geos')
		print res
		res =  es.search('pid:16388566132', index='geos', doc_type='photo_geos')
		print res

if __name__ == '__main__':
	unittest.main()