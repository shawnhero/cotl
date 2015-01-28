from kafka import KafkaClient, MultiProcessConsumer, SimpleConsumer

kafka = KafkaClient("localhost:9092")

# This will split the number of partitions among two processes
consumer = MultiProcessConsumer(kafka, "my_group", "ts",auto_commit=True,num_procs=1)

count = 0


for message in consumer:
	count = count +1;
	print(message)
	consumer.commit()
