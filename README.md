#COTL

A location-based photo sharing system.

See the following slides for data pipeline details.
[Data Pipeline](http://prezi.com/embed/nyrdqazqwfm_/?bgcolor=ffffff&amp;lock_to_path=1&amp;autoplay=0&amp;autohide_ctrls=0#)

Click into each folder to see more details.

## Overview

![alt text](http://cs.ucla.edu/~wuxu/pipeline.png)

COTL is the backend for a photo sharing application. Each user get a newsfeed consisting of photos posted by people nearby the user. The system is also able to recommend the most popular photos to users.

1. Photos are pulled out from flickr. A script runs on top of the flickr API to support live streaming data.
2. Users are synthesized. For now 1 million active users are generated to post the photos.
3. Like/view events are synthesized from each user's newsfeed. A script scans all the newsfeed for all the users and makes decisions whether to like a given photo or not.
4. Only URL(from flickr data store) is referenced in the entire system. But adding photo store can be easily integrated to the data pipeline. It is assumed that photos are stored properly before any message comes to Kafka.

## Data Stores

1. `ElasticSearch`, as a spatial database.
2. `HBase`, to store nearly all other information to be queried by our API.
3. `HDFS`, source of truth. Batch jobs are running on top of HDFS.

## Data size & Throughput

- Simulated 1 million active users.
- Streamming incoming photos from `flickr` in an average of 10 photos/second.
- Accumulated over 1 million photos.
- Simulated over 1 billion user behaviors.

I've stopped the simulation part so it should be all static data by the time you look at the system. Also I didn't spend too much time developing a web user-interface so we can actually post a photo or like a photo. It's more worth it to develop a mobile client and make a real impact.

## Scalability

It is really cool to scale something-- even my data hasn't hit the bottleneck of the original.

- 5 nodes are run in `AWS` as a cluster.
- `HBase`: 1 master, 4 datanodes.
- `ElasticSearch`: 5 shards, 1 replication each.
- `HDFS`: 1 namenode, 4 datanodes.
- `Kafka`: 1 producer, 1 broker, 2 partitions for each topic, and 2 consumers on different machines for each consumer group.





