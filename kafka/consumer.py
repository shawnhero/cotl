# A simple consumer in kafka
from kafka import KafkaClient, SimpleConsumer

kafka = KafkaClient("localhost:9092")
# To consume messages
consumer = SimpleConsumer(kafka, "my-group", "my-topic")

for message in consumer:
    # message is raw byte string -- decode if necessary!
    # e.g., for unicode: `message.decode('utf-8')`
    print(message)

kafka.close()
