# A simple consumer test
from kafka import KafkaClient, MultiProcessConsumer
import sys

if __name__ == "__main__":
	if len(sys.argv)!=2:
		print "Usage: [*.py] [topicname]"
		sys.exit(0)
	kafka = KafkaClient("localhost:9092")
	# To consume messages
	consumer = MultiProcessConsumer(kafka, "m_group", sys.argv[1],auto_commit=True,num_procs=1)
	for message in consumer:
		# message is raw byte string -- decode if necessary!
		# e.g., for unicode: `message.decode('utf-8')`
		print(message)
		consumer.commit()
	kafka.close()
