from kafka import KafkaClient, MultiProcessConsumer, SimpleConsumer
import sys


if __name__ == "__main__":
	if len(sys.argv)!=2:
		print "Usage: [*.py] [topicname]"
		sys.exit(0)
	kafka = KafkaClient("localhost:9092")
	# This will split the number of partitions among two processes
	consumer = SimpleConsumer(kafka, "newgroup", sys.argv[1])
	count = 0


	for message in consumer:
		count = count +1;
		print(message.message.value)
		print consumer.offsets
		consumer.commit()
