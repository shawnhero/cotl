## 1. Get the new photo data from flickr and stream them
## 2. Assign each photo with a user (user data pre-loaded)
## 3. Send the Photo to S3
## 4. Send the information to kafka

## to do, add control of the throughout
## Mode 0, natural mode, real stream from flickr
## Mode 1, given a number to control the number of photos streaming out
import threading
import flickrapi
import json
import time
import numpy as np
import sys
import md5
from kafka import KafkaClient, SimpleProducer


def de_encode(input):
	if not isinstance(input, unicode):
		try:
			input = input.decode("utf-8", "mixed")
		except Exception as e:
			raise
	input = input.replace('"', ' ').replace("'", ' ').replace('\n',' ').replace('\t',' ')
	return input.encode('ascii','ignore')

class ProduceMsg(threading.Thread):
	def __init__(self,pid,secret,api_key, api_secret, producer, topic_name, user_geos):
		threading.Thread.__init__(self)
		self.pid = pid
		self.secret = secret
		self.api_key = api_key
		self.api_secret = api_secret
		self.producer = producer
		self.topic_name = topic_name
		self.user_geos = user_geos
	def run(self):
		try:
			# get the detailed information 
			flickr = flickrapi.FlickrAPI(self.api_key, self.api_secret, format='json')
			# extract info from the parsed json
			raw_json =  flickr.photos.getInfo(photo_id=self.pid, secret=self.secret)
			# do the decoding below
			photo_info = json.loads(raw_json)
			pid = photo_info['photo']['id']

			title = photo_info['photo']['title']['_content']
			title = de_encode(title)

			description = photo_info['photo']['description']['_content']
			description = de_encode(description)

			tags = [ de_encode( t['_content']) for t in photo_info['photo']['tags']['tag']]

			tags = ','.join(tags)

			URL = "https://farm"+str(photo_info['photo']['farm'])+".staticflickr.com/"+str(photo_info['photo']['server'])+"/"+str(pid)+"_"+str(self.secret)+"_b.jpg"
			timeposted = photo_info['photo']['dates']['posted']
			# to add: store the file to S3
			# construct dict
			user_id =  np.random.randint(0,self.user_geos.shape[0])
			print 'send by user', user_id
			photo_dict = {}
			photo_dict['data'] = {
				"action": "post", 
				'user_id': user_id,
				"photo": {
					'pid': int(pid),
					'title': title, 
					'description': description,
					'tags': tags,
					'URL': URL,
					'timeposted': int(timeposted),
					'location': 
					{
						'latitude': self.user_geos[user_id, 1], 
						'longitude': self.user_geos[user_id, 2]
					}
				}
			}
			raw_data = json.dumps(photo_dict)
			print raw_data
			# send to the producer
			self.producer.send_messages(self.topic_name, raw_data)
		except Exception as e:
			print str(e)
			return
		
		

class StreamOut():
	def __init__(self, num_per_second, user_geos, kafkahost, topic_name, api_keys, api_secrets, ttr):
		self.num_per_second = num_per_second
		self.kafka = KafkaClient(kafkahost)
		self.producer = SimpleProducer(self.kafka)
		self.topic_name = topic_name
		self.user_geos = user_geos
		self.num_users = user_geos.shape[0]
		# set the keys and secrets
		self.api_keys = [key.decode('unicode-escape') for key in api_keys]
		self.api_secrets = [secret.decode('unicode-escape') for secret in api_secrets]
		self.ttr = ttr # -1 means infinite
	# # send data to kafka
	# print 'pushing', raw_data
	# producer.send_messages("ts", raw_data)
	def simulate_photo_detail(self, pid):
		user_id =  np.random.randint(0,self.num_users)
		photo_dict = {}
		photo_dict['data'] = {
			"action": "post", 
			'user_id': user_id,
			"photo": {
				'pid': int(pid),
				'title': 'random title:'+str(np.random.randint(0,1000)), 
				'description': 'random description:'+str(np.random.randint(0,1000)), 
				'tags': ['hello', 'world'],
				'URL': 'http://c0tl.com/images/luxi'+str(pid%6)+'.jpg',
				'timeposted': int( time.time()),
				'location': 
				{
					'latitude': self.user_geos[user_id, 1], 
					'longitude': self.user_geos[user_id, 2]
				}
			}
		}
		raw_data = json.dumps(photo_dict)
		return raw_data
	def run(self):
		# when the throughput number is greater than 3
		# we fake all the data
		pid = 0
		if self.num_per_second>3:
			while self.ttr>0:
				for i in range(self.num_per_second):
					photo_msg = self.simulate_photo_detail(pid)
					pid = pid + 1
					print photo_msg
					self.producer.send_messages(self.topic_name, photo_msg)
				time.sleep(1)
				self.ttr -= 1
			return
		# otherwise we use the data from flickr
		# specifically, the number == 0 indicates a natural mode

		api_num = np.random.randint(0,len(self.api_keys))
		api_key = self.api_keys[api_num]
		api_secret = self.api_secrets[api_num]

		# mantian two dicts to generate streaming data
		# one dict would be enough for small data
		# but as data grows bigger in memory it will crash the program
		pre_dict = {}
		cur_dict = {}
		d_size = 200
		time_runned = 0
		while True:
			flickr = flickrapi.FlickrAPI(api_key, api_secret, format='json')
			try:
				raw_json = flickr.photos.getRecent(per_page='50')
				parsed = json.loads(raw_json.decode('utf-8'))
			except UnicodeDecodeError:
				# flickr api will complain such error, anyway just wait a few seconds
				# and retry
				print str(e)
				time.sleep(10)
				continue
			count = 0
			pre_useful = False
			batch_count = 0
			for p in parsed['photos']['photo']:
				pid = str(p['farm']) + str(p['server']) + str(p['id'])
				existed = False
				if pre_dict is not None:
					if pid in pre_dict:
						existed = True
						pre_useful = True
				if pid in cur_dict:
					existed = True
				if not existed:
					cur_dict[pid] = True
					# when the throughput number is <= 3,
					# and we have alread sent over 3 photos
					# we no longer send the photos within this second
					if self.num_per_second!=0 and self.num_per_second <= 3 and batch_count>=self.num_per_second:
						continue
					# start a thread and send the message to kafka
					new_api_num = np.random.randint(0,len(self.api_keys))
					api_key = self.api_keys[api_num]
					api_secret = self.api_secrets[api_num]

					thread = ProduceMsg(
						p['id'], p['secret'], 
						self.api_keys[new_api_num], 
						self.api_secrets[new_api_num],
						self.producer,
						self.topic_name,
						self.user_geos)
					thread.start()
					#sendout(p['id'], p['secret'])
					count = count + 1
					batch_count = batch_count + 1
			if pre_dict is not None:
				if not pre_useful:
					# print "pre dict no longer useful, deleting.."
					pre_dict = None
			if len(cur_dict)>=d_size:
				# print "current dict full", len(cur_dict), ", switching.."
				pre_dict = cur_dict
				cur_dict = {}
			# print count, "New come in 1 second"
			time.sleep(1)
			time_runned = time_runned + 1
			# control the time to run
			if self.ttr>0:
				if time_runned >= self.ttr:
					return

def readkeys(path_to_file): 
	with open (path_to_file, "r") as myfile:
		data = [d.split(',') for d in myfile.read().split()]
		keys = [d[0] for d in data]
		secrets = [d[1] for d in data]
		return keys, secrets

# save to S3 and return the address
def savephoto():
	pass


def prompt_error():
	print "Usage: [*.py] [topic_name] [optional: throughput number] [optional: seconds to run]"
	sys.exit(0)

def evaluate_input():
	if len(sys.argv)>=2:
		try:
			topic = int(sys.argv[1])
		except Exception as e:
			pass
		else:
			prompt_error()
	if len(sys.argv)==2:
		# start the stream in the natural mode
		print "natural mode"
		print "topic_name:", sys.argv[1]
		num, ttr = 0, 0

	elif len(sys.argv)==3:
		try:
			num = int(sys.argv[2])
		except ValueError:
			prompt_error()
		# to do below..
		# start the stream in a controlled mode
		print "controlled mode:", 'natural' if num==0 else num
		print "time to run: infinite"
		ttr = 0
	elif len(sys.argv)==4:
		try:
			num = int(sys.argv[2])
			ttr = int(sys.argv[3])
		except ValueError:
			prompt_error()
		# to do below..
		# start the stream in a controlled mode
		print "controlled mode:", 'natural' if num==0 else num
		print "time to run:", ttr
	else:
		prompt_error()
	return sys.argv[1], num, ttr




if __name__ == "__main__":
	topic_name, num, ttr = evaluate_input()
	# preparation works
	keys, secrets = readkeys('api_keys.txt')
	user_geos = np.load('../initializations/user_geos.npy')
	kafkahost = "localhost:9092"
	stream = StreamOut(
				num,
				user_geos, 
				kafkahost, 
				topic_name,
				keys,
				secrets,
				ttr
				 )
	stream.run()