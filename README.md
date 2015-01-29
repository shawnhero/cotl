#COTL

A photo sharing system

## Overview

- Create randome users with random locations
	
	python ./fake_users/generate_user.py [number of users, default 100]

- Stream the post photo data

	python ./fake_post_photos/stream_generator.py [NUM] [TTR]

Here `NUM` means the number of photos streamed out per second. If `NUM` is set to be 0, then it will stream the photos out from flickr, which has an average number around 5 for the new photos per second. If `NUM` is set to be greater than `3`, then all the photo will be faked.

`TTR` means time-to-run(seconds). If set to 0, then the stream will run forever.

- Consume the messages
	python ./kafka_consumers/post_photo_consumer.py 

- to add...
