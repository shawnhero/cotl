import logging, time, sys, os, tempfile, json
import happybase
from kafka import KafkaClient, SimpleConsumer, MultiProcessConsumer
from pyelasticsearch.client import ElasticSearch
from webhdfs.webhdfs import WebHDFS



class BaseConsumer():
	def __init__(self,group_name, topic_name, timeout=60, filename='config.txt'):
		self.logger = logging.getLogger(__name__)
		self.logger.setLevel(logging.INFO)
		handler = logging.FileHandler('../_logs/%s.log'%group_name)
		handler.setLevel(logging.INFO)
		formatter = logging.Formatter('%(asctime)s %(message)s')
		handler.setFormatter(formatter)
		self.logger.addHandler(handler)

		try:
			f = open(filename, 'r')
			self.hbasehost = f.readline().split(' ')[0]
			self.eshost = f.readline().split(' ')[0]
			self.kafkahost = f.readline().split(' ')[0]
			self.hdfshost = f.readline().split(' ')[0]
			self.logger.info('All Hosts Loaded')
		except Exception as e:
			self.logger.warning('file load error, %s'%filename)
			self.logger.warning(str(e))
			raise
			# sys.exit(0)

		self.group_name = group_name
		self.topic_name = topic_name
		self.timeout = timeout

		try:
			self.kafka = KafkaClient(self.kafkahost)
			self.pool = happybase.ConnectionPool(size=6, host=self.hbasehost)
			self.es = ElasticSearch(self.eshost)
		except Exception as e:
			self.logger.warning(str(e))
			raise

	def run(self):
		consumer = SimpleConsumer(self.kafka, self.group_name, self.topic_name,iter_timeout=self.timeout, buffer_size=4096*8,max_buffer_size=None)
		print "setting max_buffer_size=None"
		try:
			for message in consumer:
				parsed_msg = json.loads(message.message.value)
				# print parsed_msg
				self.handle_msg(parsed_msg)
				self.logger.info('OK%s'%str(consumer.offsets))
		except Exception as e:
			print "Exception", str(e)
			self.logger.warning( "Exception %s offset, %s" % (self.group_name, consumer.offsets))
			self.logger.warning( str(e) )
			# raise
			sys.exit(0)

	def handle_msg(self, parsed_msg):
		# to be overrided
		return

if __name__ == "__main__":
	pass