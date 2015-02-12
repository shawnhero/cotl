#Initializations

## Create Tables in HBase and Indexes/Docs in ElasticSearch

```
python hbase_create.py
```

This will create 6 tables in hbase.

- `users`. To store the user information. Not active for now.
- `user_newsfeed`. To store the user newsfeeds.
- `user_posted_photos`. To store the user-photo relation.
- `user_liked_photos`. To store the user-like relation.
- `photos`. To store the photo detailed information.

For now `Denormalization` is applied to every table. That being said, `user_newsfeed` will have a complete copy of the photo detailed information. It's hard to modify a certain photo and maintain consistency. A compromise might be to store the photo id instead of the photo info copy, which brings some latency when the photos are retrieved.


```
python es_create.py
```

This will create a index and some doc types. All geo data will be explicitly indexed in `ElasticSearch`.

## Generate Users

```
python generate_users.py [NUM]
```

Create a pool of users to assign the incoming photos. The user id with be generated as numbers from `0` to `NUM-1`. Each user will be assigned with a random geo location in US.

A file will be saved locally as `user_geo.npy` for futhure reference. Also the information will be written to `HBase` and `ElasticSearch`.
