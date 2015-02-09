import sys, logging
import multiprocessing as mp
import happybase
from kafka import KafkaClient, SimpleProducer
import time, datetime
import numpy as np
import hashlib, json
import os

class ViewNewsFeed(mp.Process):
	def __init__(self, ulist, topic_name, hbasehost="c0tl.com", kafkahost="localhost:9092"):
		mp.Process.__init__(self)
		try:
			self.ulist = ulist
			self.topic_name = topic_name
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
		for t in self.ulist:
			# print t
			self.real_view( t[0], t[1], t[2])
	def view(self, uid, lat, lon):
		# scan the uid's all newsfeed
		# for each newsfeed, decide whether to like it or not
		# send the message to kafka
		uid = str(int(uid))
		return
		rowprefix = hashlib.md5(uid).digest()
		count = 0
		for key, data in self.user_newsfeed.scan(row_prefix=rowprefix):
			count += 1
	def real_view(self, uid, lat, lon):
		uid = str(int(uid))
		rowprefix = hashlib.md5(uid).digest()
		sum_count, view_count = 0, 0
		for key, data in self.user_newsfeed.scan(row_prefix=rowprefix):
			# if the photo has already been viewed
			sum_count += 1
			if 'p:viewed' in data:
				view_count +=1
				continue
			else:
				photo = json.loads(data['p:dump'])
				msg = {}
				msg['data'] = {
					"user_id": int(uid),
					"update_user_geo": 'no',
					"location":
					{
						"latitude": lat,
    					"longitude": lon
					},
					"photo": photo["photo"],
					"timeviewed": int(time.time())

				}
				if self.dice_like(photo['photo']['pid']):
					# the user liked the photo..
					msg['data']['action']="like"
					# print "UID %s liked %s"%(uid, photo['photo']['pid'])
				else:
					# the user doesn't choose to like the photo..
					msg['data']['action']="view"
					# print "UID %s viewed %s"%(uid, photo['photo']['pid'])
				self.producer.send_messages(self.topic_name, json.dumps(msg))
		print "UID %s summary:"%uid
		print "%i in total in newsfeed, %i viewed, %i handled." %(sum_count, view_count, sum_count- view_count)
	def dice_like(self, pid):
		# might write a function of pow law
		# below is just a very subjective simulation of photo quality distribution
		# 1% photos will get 100% likes
		# 9% photos will get 80% likes
		# 50% photos will get 50% likes
		# 30% photos will get 30% likes
		# 10% photos will get 10% likes
		# expectation: 0.522
		quality = int(hashlib.md5("%i"%pid).hexdigest(), 16)%100 # inherent quality
		decision = np.random.randint(0,100) # random decision
		if quality==0:
			return True
		elif quality<10:
			if decision<80:
				return True
		elif quality<60:
			if decision<50:
				return True
		elif quality<90:
			if decision<30:
				return True
		else:
			if quality<10:
				return True
		return False


# '../initializations/user_geos.npy'
# every 20 minutes, run a simulation
class AssignWorkers:
	def __init__(self, topicname,user_geo_path='../initializations/user_geos.npy', numworkers=4, waittime_after_finish=20*60):
		self.logger = logging.getLogger(__name__)
		self.logger.setLevel(logging.INFO)
		handler = logging.FileHandler('_logs/simulated_likes.log')
		handler.setLevel(logging.INFO)
		formatter = logging.Formatter('%(asctime)s %(message)s')
		handler.setFormatter(formatter)
		self.logger.addHandler(handler)

		self.topic_name = topicname
		self.waittime = waittime_after_finish
		# read the user_geo.npy as prior
		self.user_geos = np.load(user_geo_path)
		self.numworkers = numworkers
		num_perworker = self.user_geos.shape[0]/numworkers
		print "Assiging %s Workers, average %s per worker.."%(numworkers, num_perworker)
		self.ulist = [self.user_geos[i*num_perworker:(i+1)*num_perworker,:] for i in range(numworkers-1) ]
		self.ulist.append(self.user_geos[(numworkers-1)*num_perworker:,:])

		self.command0 =  "bash /home/ubuntu/Dropbox/aws/kafka_consumers/like/like.sh start "+self.topic_name
		self.command1 = "bash /home/ubuntu/Dropbox/aws/kafka_consumers/like/like.sh stop"
	def run(self):
		while True:
			print "Opening one loop to simulate likes!"
			# print "Executing...",self.command0
			# os.system(self.command0)
			pros = []
			for i in range(self.numworkers):
				p = ViewNewsFeed(self.ulist[i], topic_name=self.topic_name)
				p.start()
				pros.append(p)
			for p in pros:
				p.join()
			print 'One loop Okay, all newsfeed viewed!'
			self.logger.info('One loop Okay, all newsfeed viewed!')
			print "sleeping..20 min"
			time.sleep(self.waittime)
			# os.system(self.command1)


if __name__ == '__main__':
	if len(sys.argv)!=2:
		print "Usage: [*.py] [topicname]"
		sys.exit(0)
	test = AssignWorkers(topicname=sys.argv[1])
	test.run()
