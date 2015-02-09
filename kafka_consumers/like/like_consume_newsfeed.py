import sys, logging
logging.basicConfig(filename="../_logs/consumers.log", level=logging.CRITICAL, format='%(asctime)s %(name)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
from consume_base import BaseConsumer
from struct import pack
import json
sys.path.append("..")
from func import get_row_key


class Newsfeed_Consumer(BaseConsumer):
	def handle_msg(self, parsed_msg, num_neighbors=5):
		action = parsed_msg['data']['action']
		if action!="view" and action!="like":
			raise Exception("Unexpected action msg!")
		
		# notify the hbase that photo has been viewed
		pre_rowkey = get_row_key(
			parsed_msg['data']['user_id'],
			parsed_msg['data']['photo']['pid'],
			parsed_msg['data']['photo']['timeposted'])
		with self.pool.connection() as connection:
			user_newsfeed = connection.table('user_newsfeed')
			user_newsfeed.put(pre_rowkey,{'p:viewed':"1"})
			print "Setting Photo to be viewed.."

		# if the user just viewed the photo, do nothing
		if action=='view':
			return
		# if the user liked the photo, write it to other nearby user's newsfeed
		indexname='geos'
		doc_name='user_geos'
		tbl_name='user_newsfeed'
		# the number below will be smaller than that in 'post' topic
		lat = parsed_msg['data']['location']['latitude']
		lon = parsed_msg['data']['location']['longitude']
		lat, lon = float(lat), float(lon)
		# connect to elasticsearch and return the neighbors
		query = {
			"from" : 0, "size" : num_neighbors,
			'query': {
				 "match_all" : { }
			 },
			 "filter" : {
				"geo_distance" : {
					"distance" : "100km",
					"location" : {
						"lat" : lat,
						"lon" : lon
					}
				}
			},
			 "sort" : [
				{
					"_geo_distance" : {
						"location" :  {
							"lat" : lat,
							"lon" : lon
						},
						"order" : "asc",
						"unit" : "km"
						# ,"distance_type": "plane"
					}
				}
			]

		 }
		res =  self.es.search(query, index=indexname, doc_type=doc_name)
		## store the nearest neighbors in a list
		uids = [int(r['_id']) for r in res['hits']['hits']]
		# print len(uids), "neighbors Retrieved from ElasticSearch!"
		print "UIDs as following,\n", uids
		## connect the hbase
		# connection = happybase.Connection(hbasehost)
		with self.pool.connection() as connection:
			user_newsfeed = connection.table('user_newsfeed')
			## iterate the uids and update their newsfeed
			timeposted = int(parsed_msg['data']['photo']['timeposted'])
			pid = parsed_msg['data']['photo']['pid']
			for uid in uids:
				# rowkey is MD5(uid)+str(timestamp)+MD5(pid)
				rowkey = get_row_key(uid, pid, timeposted)
				# first we need to make sure the rowkey does not exist
				row = user_newsfeed.row(rowkey)
				if not row:
					user_newsfeed.put(
							rowkey, 
							{
								# dump the json file of the photo infor
								"p:dump": json.dumps(
									dict(photo=parsed_msg['data']['photo'])
								)
							}
						)
				
if __name__ == "__main__":
	if len(sys.argv)!=2:
		print "Usage: [*.py] [topicname]"
		sys.exit(0)
	newsfeed_consumer = Newsfeed_Consumer(
					group_name='like_newsfeed', 
					topic_name=sys.argv[1],
					timeout=60,
					filename='config.txt')
	newsfeed_consumer.run()