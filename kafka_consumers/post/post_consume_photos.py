# save the photo information
import sys, logging
logging.basicConfig(filename="../_logs/consumers.log", level=logging.CRITICAL, format='%(asctime)s %(name)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
from consume_base import BaseConsumer
from struct import pack
import json, hashlib

class Photo_Consumer(BaseConsumer):
	# given a single parsed message, add the user-photo info to the user_photos table
	def handle_msg(self, parsed_msg):
		tbl_name='photos'
		# uid = parsed_msg['data']['user_id']
		timeposted = int(parsed_msg['data']['photo']['timeposted'])
		pid = parsed_msg['data']['photo']['pid']
		rowkey = hashlib.md5(str(pid)).digest()
		## ready to write to hbase
		print pid
		with self.pool.connection() as connection:
			photos = connection.table(tbl_name)
			photos.put(	
					rowkey, 
						{
							'p:dump':json.dumps(parsed_msg)
						}, timestamp=timeposted
					)

if __name__ == "__main__":
	if len(sys.argv)!=2:
		print "Usage: [*.py] [topicname]"
		sys.exit(0)
	photo_consumer = Photo_Consumer(
					group_name='photos', 
					topic_name=sys.argv[1],
					timeout=60,
					filename='config.txt')
	photo_consumer.run()