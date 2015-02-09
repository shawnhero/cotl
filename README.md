#COTL

A location-based photo sharing system.

See the following slides for data pipeline details.
[Data Pipeline](http://prezi.com/embed/nyrdqazqwfm_/?bgcolor=ffffff&amp;lock_to_path=1&amp;autoplay=0&amp;autohide_ctrls=0#)

## Overview
###Users
40,000 users 
- Create randome users with random locations
	
    ```
	python ./simulated_users/generate_user.py [number of users, default 100]
    ```

- Stream the post photo data

    ```
	bash simulated_post_photos/stream.sh start
    ```


- Consume the messages

    ```
	bash kafka_consumers/post.sh start
    ```


