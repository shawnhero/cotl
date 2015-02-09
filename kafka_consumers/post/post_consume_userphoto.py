import sys, logging
logging.basicConfig(filename="../_logs/consumers.log", level=logging.CRITICAL, format='%(asctime)s %(name)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
from consume_base import BaseConsumer
from struct import pack
import json
sys.path.append("..")
from func import get_row_key

class UserPhoto_Consumer(BaseConsumer):
	# given a single parsed message, add the user-photo info to the user_photos table
	def handle_msg(self, parsed_msg):
		tbl_name = 'user_posted_photos'
		with self.pool.connection() as connection:
			uid = parsed_msg['data']['user_id']
			pid = parsed_msg['data']['photo']['pid']
			timeposted = parsed_msg['data']['photo']['timeposted']
			rowkey = get_row_key(uid, pid, timeposted, uidfirst=True)
			## ready to write to hbase
			user_photos = connection.table(tbl_name)
			user_photos.put(
					rowkey, 
						{'p:dump': json.dumps(
							dict(photo=parsed_msg['data']['photo'])
							),
						}, timestamp=int(timeposted)
					)


if __name__ == "__main__":
	if len(sys.argv)!=2:
		print "Usage: [*.py] [topicname]"
		sys.exit(0)
	userphoto_consumer = UserPhoto_Consumer(
					group_name='userphoto', 
					topic_name=sys.argv[1],
					timeout=60,
					filename='config.txt')
	userphoto_consumer.run()