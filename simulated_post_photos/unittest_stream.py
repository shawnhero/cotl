import random
import unittest
import numpy
from stream_generator import *


# run unit tests for all the consumer workers
class TestStreamGenerator(unittest.TestCase):

	def setUp(self):
		self.path = 'api_keys.txt'
		self.user_geos = np.load('../fake_users/user_geos.npy')
		self.kafkahost = "localhost:9092"
		self.keys, self.secrets = readkeys(self.path)
	def test_readkeys(self):
		print '-'*50
		print 'Testing readkeys..'
		print '-'*50
		keys, secrets = readkeys(self.path)
		self.assertEqual(len(keys), len(secrets))
		self.assertTrue(len(keys)>0)
	def test_natrual_mode(self):
		print '-'*50
		print 'Testing natrual mode..'
		print '-'*50
		stream = StreamOut(
				0,
				self.user_geos, 
				self.kafkahost, 
				'post_photos',
				self.keys,
				self.secrets,
				1
				 )
		stream.run()
		# after 3 seconds the producer will stop
	def test_num_3_mode(self):
		n ,num = 1,2
		print '-'*50
		print 'Testing stream generator..'
		print 'expect', num, 'messages per second, flowing for',n, 'seconds'
		print '-'*50
		stream = StreamOut(
				num,
				self.user_geos, 
				self.kafkahost, 
				'post_photos',
				self.keys,
				self.secrets,
				n
				 )
		stream.run()
		# after 3 seconds the producer will stop

	def test_num_20_mode(self):
		n ,num = 2,5
		print '-'*50
		print 'Testing stream generator..'
		print 'expect', num, 'messages per second, flowing for',n, 'seconds'
		print '-'*50
		stream = StreamOut(
				num,
				self.user_geos, 
				self.kafkahost, 
				'post_photos',
				self.keys,
				self.secrets,
				n
				 )
		stream.run()
		# after 3 seconds the producer will stop

if __name__ == '__main__':
	unittest.main()