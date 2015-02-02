import sys, logging
logging.basicConfig(filename="../_logs/consumers.log", level=logging.CRITICAL, format='%(asctime)s %(name)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
from consume_base import BaseConsumer
from struct import pack
import json

class UserPhoto_Consumer(BaseConsumer):
	# given a single parsed message, add the user-photo info to the user_photos table
	def handle_msg(self, parsed_msg):
		tbl_name = 'user_photos'
		with self.pool.connection() as connection:
			# column qualifier is timestamp+photoID
			# 10 Byte + 8 Byte = 18 Byte, which is not too bad
			col_qualifier = str(parsed_msg['data']['photo']['timeposted']) + str(parsed_msg['data']['photo']['pid'])
			rowkey = pack('Q', parsed_msg['data']['user_id'])
			timeposted = int(parsed_msg['data']['photo']['timeposted'])
			## ready to write to hbase
			# connection = happybase.Connection(hbasehost)
			user_photos = connection.table(tbl_name)
			## the columnqualifier has enough information
			## for now the value is only
			user_photos.put(
					rowkey, 
						{'posted_photos:'+col_qualifier: json.dumps(parsed_msg),
						}, timestamp=timeposted
					)


if __name__ == "__main__":
	if len(sys.argv)!=2:
		print "Usage: [*.py] [topicname]"
		sys.exit(0)
	userphoto_consumer = UserPhoto_Consumer(
					group_name='userphoto', 
					topic_name=sys.argv[1],
					timeout=5,
					filename='config.txt')
	userphoto_consumer.run()