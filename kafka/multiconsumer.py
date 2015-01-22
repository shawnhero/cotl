from kafka import KafkaClient, MultiProcessConsumer

kafka = KafkaClient("localhost:9092")

# This will split the number of partitions among two processes
consumer = MultiProcessConsumer(kafka, "my-group", "new-topic", num_procs=2)

for message in consumer.get_messages(count=5):
	print(message.message.value)


class Likes:
	pass

class Post:
	pass

class UpdateGeo:
	pass

class 