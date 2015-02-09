import sys, logging
logging.basicConfig(filename="../_logs/consumers.log", level=logging.CRITICAL, format='%(asctime)s %(name)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
from consume_base import BaseConsumer
from struct import pack
import json
sys.path.append("..")
from func import get_row_key


class Newsfeed_Consumer(BaseConsumer):
	def handle_msg(self, parsed_msg):
		print parsed_msg
		indexname='geos'
		doc_name='user_geos'
		tbl_name='user_newsfeed'
		num_neighbors=10
		lat = parsed_msg['data']['photo']['location']['latitude']
		lon = parsed_msg['data']['photo']['location']['longitude']
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
		print len(uids), "neighbors Retrieved from ElasticSearch!"
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
				# col_qualifier = str(timeposted)+str(pid)
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
					group_name='newsfeed', 
					topic_name=sys.argv[1],
					timeout=60,
					filename='config.txt')
	newsfeed_consumer.run()