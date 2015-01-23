## consume the message from kafka

## 1. Send the 'user post photo' event/other relations to HBase
## 2. Send the 'user is at location' infor to Solr
## 3. Retrieve nearyby users and add the photo to their newsfeed 
## 6. Send the actual photo to S3

from kafka import KafkaClient, MultiProcessConsumer

kafka = KafkaClient("localhost:9092")

# This will split the number of partitions among two processes
consumer = MultiProcessConsumer(kafka, "my_group", "post_photos", num_procs=5)

count = 0
while True:
	for message in consumer:
		count = count +1;
		print "Message", count, ':\n', message.message.value
