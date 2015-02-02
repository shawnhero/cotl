import sys, logging
logging.basicConfig(filename="../_logs/consumers.log", level=logging.CRITICAL, format='%(asctime)s %(name)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
from consume_base import BaseConsumer
from struct import pack
import json

class Photo_Consumer(BaseConsumer):
	# given a single parsed message, add the user-photo info to the user_photos table
	def handle_msg(self, parsed_msg):
		tbl_name='photos'
		# pack the user/photo id as unsigned long long, which takes 8 Bytes
		rowkey = pack('Q', int(parsed_msg['data']['photo']['pid']))
		postby = pack('Q', parsed_msg['data']['user_id'])
		born_lat = pack('d', parsed_msg['data']['location']['latitude'])
		born_lon = pack('d', parsed_msg['data']['location']['longitude'])
		tags = parsed_msg['data']['photo']['tags']
		# pack it
		title = parsed_msg['data']['photo']['title']
		description = parsed_msg['data']['photo']['description']
		url = parsed_msg['data']['photo']['URL']
		timeposted = int(parsed_msg['data']['photo']['timeposted'])
		## ready to write to hbase
		with self.pool.connection() as connection:
			photos = connection.table(tbl_name)
			photos.put(	
					rowkey, 
						{	'metrics:numLiked': pack('i',0),
							'metrics:numViewed': pack('i',0),
							'details:postby': postby,
							'details:born_lat': born_lat,
							'details:born_lon': born_lon,
							'details:tags':  tags,
							'details:title': title,
							'details:description': description,#.decode('utf-8'),
							'details:url': url,
							'details:timeposted': pack('i', timeposted)
						}, timestamp=timeposted
					)
			


if __name__ == "__main__":
	if len(sys.argv)!=2:
		print "Usage: [*.py] [topicname]"
		sys.exit(0)
	photo_consumer = Photo_Consumer(
					group_name='photos', 
					topic_name=sys.argv[1],
					timeout=5,
					filename='config.txt')
	photo_consumer.run()