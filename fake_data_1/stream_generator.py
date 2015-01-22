import flickrapi
import json
import time
import numpy as np

# send out the incoming streaming data
# send to kafka as a producer
def sendout(uid, data):
	return


api_key = u'5fcf00d1facf3e9352b1945607eb690a'
api_secret = u'150e0c952c4ee6e6'

pre_dict = {}
cur_dict = {}
d_size = 200
detect_size = 3600
data = np.empty(detect_size-1, dtype=int)
for i in range(detect_size):
	flickr = flickrapi.FlickrAPI(api_key, api_secret, format='json')
	raw_json = flickr.photos.getRecent(per_page='50')
	parsed = json.loads(raw_json.decode('utf-8'))
	count = 0
	pre_useful = False
	for p in parsed['photos']['photo']:
		uid = str(p['farm']) + str(p['server']) + str(p['id'])
		existed = False
		if pre_dict is not None:
			if uid in pre_dict:
				existed = True
				pre_useful = True
		if uid in cur_dict:
			existed = True
		if not existed:
			cur_dict[uid] = True
			sendout(uid, p)
			count = count + 1
	if not pre_dict is None:
		if not pre_useful:
			print "pre dict no longer useful, deleting.."
			pre_dict = None
	if len(cur_dict)>=d_size:
		print "current dict full", len(cur_dict), ", switching.."
		pre_dict = cur_dict
		cur_dict = {}
	if i>0:
		print count, "New come in 1 second"
		data[i-1] = count
	time.sleep(1)
np.save('time_data',data)

