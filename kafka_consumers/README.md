#Consumers

##Post

A typical `post` message is as follows,

```
    {"data": 
        {
            "action": "post", 
            "user_id": 95,
            "photo": 
            {
                "pid": 16385653535,
                "URL": "https://farm9.staticflickr.com/8587/16196839837_44646d4a3b_b.jpg", 
                "tags": ["midville", "middlevillage", "tumblr", "11379"], 
                "description": "via Tumblr <a href=\\"http://ift.tt/1CdzfgB\\" rel=\\"nofollow\\">ift.tt/1CdzfgB</a>", 
                "title": "#Maspeth #maspethqueens by candicehuezo http://ift.tt/1CvJCLi",
                'timeposted': 1422390701,
                "location": 
                {
                   "latitude": 37.488165001918695, 
                    "longitude": -122.35799719884271
                }
            }
        }
    }
```

5 consumers will consume the same topic `post`.

1. Update the user's location in `ElasticSearch`.
2. Search `10` nearest users of the poster, then push the photo to the users' newsfeed, which is a table in `HBase`.
3. Save the user-post relation in `HBase`.
4. Save the photoID-details relation in `HBase`.
5. Dump the message as a tab-delimited line in `HDFS`.

After all that, the following queries can be answered,

1. Given a user ID, what's the user's newsfeed?
2. Given a photo ID, what's the detailed information?
3. Given a user ID, what are the photos that the users has posted?


##Like

A typical `like` message is as follow,

```
    {"data": 
        {
            "action": "like", 
            "user_id": 95, 
            "location":
            {
                "latitude": 39.5000,
                "longitude": -123.3356
            },
            "update_user_geo": 'no',
            "photo": 
            {
                "pid": 16385653535,
                "URL": "https://farm9.staticflickr.com/8587/16196839837_44646d4a3b_b.jpg", 
                "tags": ["midville", "middlevillage", "tumblr", "11379"], 
                "description": "via Tumblr <a href=\\"http://ift.tt/1CdzfgB\\" rel=\\"nofollow\\">ift.tt/1CdzfgB</a>", 
                "title": "#Maspeth #maspethqueens by candicehuezo http://ift.tt/1CvJCLi",
                'timeposted': 1422390701,
                "location": 
                {
                   "latitude": 37.488165001918695, 
                    "longitude": -122.35799719884271
                }
            }
        }
    }
```

4 consumers will consume the same topic `like`.

1. Update the user's location in `ElasticSearch`.
2. Search `5` nearest users of the liker, then push the photo to the users' newsfeed, which is a table in `HBase`.
3. Save the user-like relation in `HBase`.
4. Dump the message as a tab-delimited line in `HDFS`.

After all that, the following queries can be answered,

1. Given a user ID, what's the user's newsfeed?
2. Given a user ID, what are the photos that the users has liked?




