import sys
import logging
logging.basicConfig(filename="../_logs/consumers.log", level=logging.ERROR, format='%(asctime)s %(name)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
from consume_base import BaseConsumer
from struct import pack
import json
from webhdfs.webhdfs import WebHDFS
import os, tempfile
import time
from datetime import datetime

class HDFS_Consumer(BaseConsumer):
	# given a single parsed message, add the user-photo info to the user_photos table
	def __init__(self,group_name, topic_name, max_tmp_size=50,timeout=15, filename='config.txt'):
		BaseConsumer.__init__(self,group_name, topic_name,timeout=timeout, filename=filename)
		self.ftmp = tempfile.NamedTemporaryFile()
		# max_tmp_size comes in unit of MB
		self.max_tmp_size = max_tmp_size*1000*1000
		self.webhdfs = WebHDFS("c0tl.com", 50070, "hdfs")
	# given a dict msg, flatten it to tab delimited string
	def flatten_msg(self, parsed_msg):
		msg = parsed_msg['data']['action'] + '\t' + \
				"%s" % parsed_msg['data']['user_id'] + '\t' +\
				"%s" % parsed_msg['data']['photo']['pid'] + '\t' + \
				"%.15f" % parsed_msg['data']['photo']['location']['latitude'] + '\t' +\
				"%.15f" % parsed_msg['data']['photo']['location']['longitude'] + '\t' +\
				parsed_msg['data']['photo']['URL'] + '\t' +\
				parsed_msg['data']['photo']['title'] + '\t' +\
				parsed_msg['data']['photo']['description'] + '\t' +\
				parsed_msg['data']['photo']['tags'] + '\t' +\
				"%s" % parsed_msg['data']['photo']['timeposted'] + '\n'
		return msg

	def handle_msg(self, parsed_msg):
		msg = self.flatten_msg(parsed_msg)
		print msg
		self.ftmp.write(msg)
		# if the tmp file size exceeds certain limits, flush it to HDFS
		if self.ftmp.tell()>self.max_tmp_size:
			self.flush_to_hdfs()

	def flush_to_hdfs(self):
		print "Flushing.."
		self.logger.info("Flushing tmp file")
		self.ftmp.flush()
		self.logger.info("Copying to HDFS..")
		# use the currrent timestamp as the hdfs file name
		hdfs_name = datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')
		self.webhdfs.copyFromLocal(self.ftmp.name, "/user/photo_dump/post/%s.dat"%hdfs_name)
		self.ftmp.close()
		# create new temp file
		self.ftmp = tempfile.NamedTemporaryFile()
	
	def __del__(self):
		# before it exits, write the last file to hdfs
		self.logger.info("Exit Cleaning..")
		self.flush_to_hdfs()
		self.ftmp.close()


if __name__ == "__main__":
	if len(sys.argv)!=2:
		print "Usage: [*.py] [topicname]"
		sys.exit(0)
	photo_consumer = HDFS_Consumer(
					group_name='hdfs_dump', 
					topic_name=sys.argv[1])
	photo_consumer.run()