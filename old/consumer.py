from kafka import KafkaClient, SimpleConsumer


# To consume messages
consumer = SimpleConsumer(kafka, "my-group", "my-topic")
for message in consumer:
    # message is raw byte string -- decode if necessary!
    # e.g., for unicode: `message.decode('utf-8')`
    print(message)

kafka.close()