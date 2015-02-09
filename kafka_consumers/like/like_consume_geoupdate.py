import sys, logging
logging.basicConfig(filename="../_logs/consumers.log", level=logging.CRITICAL, format='%(asctime)s %(name)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
from consume_base import BaseConsumer

class Geo_Consumer(BaseConsumer):
	def handle_msg(self, parsed_msg):
		# given a single parsed message, index the user's location as well as the photo's location in elastic search
		if parsed_msg['data']['update_user_geo']=='no':
			return
		indexname='geos'
		user_type='user_geos'
		user_doc = {
			'uid': int(parsed_msg['data']['user_id']),
			"location" : {
	 			"lat" : parsed_msg['data']['location']['latitude'],
	 			"lon" : parsed_msg['data']['location']['longitude']
	 		}
		}
		self.es.index(indexname, user_type, user_doc)

if __name__ == "__main__":
	if len(sys.argv)!=2:
		print "Usage: [*.py] [topicname]"
		sys.exit(0)
    # logging.basicConfig(filename='error.log',level=logging.DEBUG)
	
	# logger = logging.getLogger('geo_app')
	# # create file handler which logs even debug messages
	# fh = logging.FileHandler('geoupdate.log')
	# fh.setLevel(logging.INFO)
	# logger.addHandler(fh)
	geo_consumer = Geo_Consumer(
					group_name='geoupdate', 
					topic_name=sys.argv[1],
					timeout=21*60,
					filename='config.txt')
	geo_consumer.run()