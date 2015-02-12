#Simulated Posts

Flickr API has a support to query the most recent `[N]` photos. The `stream_generator.py` will send a query in every one second, asking 50 recent photos, maintain two dicts to keep track of the overlapped data, and eventually stream the data out to `Kafka`.

Note, each time we will assign a photo with a user ID to indicate `post` relation. The range of the user ID is retrieved from the `user_geos.npy` file we created in the `initialization` step.

## Usage

```
    python stream_generator.py [topic_name] [optional: throughput number] [optional: seconds to run]
```

- Throughput number. By default `0`, meaning a natrual flow of the flick data. If the number is below `4` then it will limit the number of messages sending out per second. Otherwise it will not use the flickr data as incoming data-- instead, it will replay seveal static images, assign them to random users and then send the message to `Kafka` with the throughput specified.
- Seconds to run. By default `0`, meaning `forever`. Otherwise it will terminate after the time specified.