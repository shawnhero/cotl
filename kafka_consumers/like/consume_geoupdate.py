import sys, logging
logging.basicConfig(filename="../_logs/consumers.log", level=logging.CRITICAL, format='%(asctime)s %(name)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
from consume_base import BaseConsumer

class Geo_Consumer(BaseConsumer):
	def handle_msg(self, parsed_msg):
		# given a single parsed message, index the user's location as well as the photo's location in elastic search
		indexname='geos'
		user_type='user_geos'
		photo_type='photo_geos'
		# establish a connection to ElasticSearch
		user_doc = {
			'uid': int(parsed_msg['data']['user_id']),
			"location" : {
	 			"lat" : parsed_msg['data']['location']['latitude'],
	 			"lon" : parsed_msg['data']['location']['longitude']
	 		}
		}
		photo_doc = {
			'pid': int(parsed_msg['data']['photo']['pid']),
			"location" : {
	 			"lat" : parsed_msg['data']['location']['latitude'],
	 			"lon" : parsed_msg['data']['location']['longitude']
	 		}
		}
		self.es.index(indexname, user_type, user_doc)
		self.es.index(indexname, photo_type, photo_doc)


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
					timeout=5,
					filename='config.txt')
	geo_consumer.run()