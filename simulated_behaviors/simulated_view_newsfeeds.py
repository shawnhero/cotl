import sys, multiprocessing
import happybase
from kafka import KafkaClient, SimpleProducer
import time, datetime

class ViewNewsFeed(multiprocessing.Process):
	def __init__(self, row_start, row_stop hbasehost="c0tl.com", kafkahost="localhost:9092"):
		multiprocessing.Process.__init__(self)
		try:
			self.row_start = row_start
			self.row_stop = row_stop
			self.connection = happybase.Connection(hbasehost)
			self.user_newsfeed = self.connection.table('user_newsfeed')
			self.kafka = KafkaClient(kafkahost)
			self.producer = SimpleProducer(self.kafka)
		except Exception as e:
			print str(e)
			sys.exit(0)

	def run(self):
		# iterate the viewed list
		# construct a dict
		for key, data in self.user_newsfeed.scan(row_start=self.row_start, row_stop=self.row_stop):
			
		# iterate the userlist
		# scan all the columns of the uid
		# consume the 
		for key, data in table.scan(row_start='aaa', row_stop='xyz'):
			print key, data
	def viewed(uid, pid, liked=False):
		# send the message to kafka

if __name__ == '__main__':
	jobs = []
	for i in range(5):
		p = Worker()
		jobs.append(p)
		p.start()
	for j in jobs:
		j.join()
