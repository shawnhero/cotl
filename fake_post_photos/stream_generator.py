## 1. Get the new photo data from flickr and stream them
## 2. Assign each photo with a user (user data pre-loaded)
## 3. Send the Photo to S3
## 4. Send the information to kafka
import threading
import flickrapi
import json
import time
import numpy as np
import sys
import md5
from kafka import KafkaClient, SimpleProducer

user_geos = np.load('user_geos.npy')
kafka = KafkaClient("localhost:9092")
producer = SimpleProducer(kafka)

def sendout(pid, secret):
	# first get the detailed information 
	api_key = u'5fcf00d1facf3e9352b1945607eb690a'
	api_secret = u'150e0c952c4ee6e6'
	flickr = flickrapi.FlickrAPI(api_key, api_secret, format='json')
	# extract info from the parsed json
	raw_json =  flickr.photos.getInfo(photo_id=pid, secret=secret)
	photo_info = json.loads(raw_json.decode('utf-8'))
	pid = photo_info['photo']['id']
	title = photo_info['photo']['title']['_content']
	description = photo_info['photo']['description']['_content']
	tags = [t['_content'] for t in photo_info['photo']['tags']['tag']]
	URL = "https://farm"+str(photo_info['photo']['farm'])+".staticflickr.com/"+str(photo_info['photo']['server'])+"/"+str(pid)+"_"+str(secret)+"_b.jpg"
	timeposted = photo_info['photo']['dates']['posted']

	# to add: store the file to S3

	# construct dict
	user_id =  np.random.randint(0,100)
	mydict = {}
	mydict['data'] = {}
	mydict['data']['user_id'] = user_id
	mydict['data']['action'] = 'post'
	mydict['data']['location'] = {'latitude': user_geos[user_id, 1], 'longitude': user_geos[user_id, 2]}
	mydict['data']['photo'] = {
		'pid': int(pid),
		'title':title, 
		'description': description, 
		'tags': tags,
		'URL': URL,
		'timeposted': int(timeposted)
	}
	raw_data = json.dumps(mydict)

	# send data to kafka
	print 'pushing', raw_data
	producer.send_messages("ts", raw_data)

	return

# save to S3 and return the address
def savephoto():
	pass

if __name__ == "__main__":
	api_key = u'5fcf00d1facf3e9352b1945607eb690a'
	api_secret = u'150e0c952c4ee6e6'

	# mantian two dicts to generate streaming data
	# one dict would be enough for small data
	# but as data grows bigger in memory it will crash the program
	pre_dict = {}
	cur_dict = {}
	d_size = 200
	# data = np.empty(detect_size-1, dtype=int)
	while True:
		flickr = flickrapi.FlickrAPI(api_key, api_secret, format='json')
		raw_json = flickr.photos.getRecent(per_page='50')
		parsed = json.loads(raw_json.decode('utf-8'))
		count = 0
		pre_useful = False
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
				thread = threading.Thread(target=sendout, args=(p['id'], p['secret'],))
				thread.start()
				#sendout(p['id'], p['secret'])
				count = count + 1
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