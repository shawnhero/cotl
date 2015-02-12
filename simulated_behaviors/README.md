#Simulated Likes/Views

The script is a multiprocess simulator.

First, it reads the `user_geos.npy` file we generated in the `initilization` step. Then split the work to several workers.

Second, each worker will have a list of UIDs to scan. By scanning the users' newsfeed, the worker made the decision whether to like the photo or not, and send the message back to `Kafka`.


##Assumptions

1. There's no aesthetical difference for the users.
2. Each photo has an inherent quality factor to measure its quality.

Actually, as you might find out from the code, I defined the quality factor to be,

```
int(hashlib.md5("%i"%pid).hexdigest(), 16)%100 
```

and enfored a photo quality distribution to simulate the user behaviors as real as possible.