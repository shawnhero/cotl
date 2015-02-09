#!/usr/bin/python
from flask import Flask, request, json
import flask
import happybase
from pyelasticsearch.client import ElasticSearch
import hashlib
hbasehost = 'c0tl.com'
from struct import *
app = Flask(__name__)
es = ElasticSearch('http://localhost:9200/')
POOL = happybase.ConnectionPool(size=30, host="c0tl.com")

#retrieve all the photos
def get_row_prefix(uid, timestamp=None):
	prefix = hashlib.md5(str(uid)).digest()
	if timestamp:
		prefix += str(timestamp)
	print "Prefix:",prefix
	return prefix
	

# APIs offered by flask

@app.route('/')
def home():
	return """<html>
  <h2>Welcome to the colt API!</h2>
</html>"""

# given a user id, return the newsfeed
@app.route('/uid/<userid>')
def newsfeed(userid):
	# return userid
	try:
		uid = int(userid)
	except ValueError:
		return "Invalid uid"
	# connect to HBase and return the newsfeed
	alldata = {}
	with POOL.connection() as connection:
		# connection = happybase.Connection(hbasehost)
		user_newsfeed = connection.table('user_newsfeed')
		count = 0
		for key, data in user_newsfeed.scan(row_prefix=get_row_prefix(userid)):
			# skip those viewed photos
			if 'p:viewed' in data:
				continue
			alldata[count] = json.loads(data["p:dump"])
			count +=1
	return json.dumps(alldata)


# return the distribution of the number of newsfeed
@app.route('/dist')
def dist_newsfeed():
	return 0


# given a location, return the most popular photos
@app.route('/nearby/', methods=['POST'])
def nearby():
	lat=request.form['lat']
	lon=request.form['lon']
	r = request.form['r'] 
	query = {
		"from" : 0, "size" : 300,
		'query': {
			 "match_all" : { }
		 },
		 "filter" : {
			"geo_distance" : {
				"distance" : str(r)+'km',
				"location" : {
					"lat" : lat,
					"lon" : lon
				}
			}
		},
		 "sort" : [
			{
				"_geo_distance" : {
					"location" :  {
						"lat" : lat,
						"lon" : lon
					},
					"order" : "asc",
					"unit" : "km"
				}
			}
		]
	 }
	# retrieve data from es
	res =  es.search(query, index='photo_geos',doc_type=['photos'])
	pids = [ [ int(r['_source']['likes']), int(r['_source']['views']), r['_id'],r['sort'][0], r['_source']['location']['lat'], r['_source']['location']['lon'] ] for r in res['hits']['hits']]
	pids.sort(reverse=True)
	# list of 
	# like, view, pid, distance, lat, lon
	result = {}
	count = 0
	with POOL.connection() as connection:
		ptbl = connection.table('photos')
		for p in pids:
			result['%04d'%count] = {
				"distance": float(p[3]),
				"numLiked": int(p[0]),
				"numViewed": int(p[1])
			}
			rowkey = hashlib.md5(str(p[2])).digest()
			result['%04d'%count]['photo'] = json.loads( ptbl.row(rowkey)['p:dump'] )['data']['photo']
			count += 1
	return json.dumps(result)
	# retrieve the photo info from hbase

# given a hashtag, return the photos linked with that
@app.route('/tag/', methods=['POST'])
def tag():
	tagname=request.form['name']
	count=request.form['num']
	rowkey = "%016d"%int(count) + hashlib.md5(tagname).digest()
	connection = happybase.Connection(hbasehost)
	tag_tbl = connection.table('top_tags')
	return tag_tbl.row(rowkey)['p:dump']

# given a photo id, return the detailed information


# return the most popular hashtags
@app.route('/top_tags')
def trending_hashtags():
	connection = happybase.Connection(hbasehost)
	tag_tbl = connection.table('top_tags')
	tag_dict = {}
	pairs = []
	for key, data in tag_tbl.scan():
		pairs.append([key, data])
	for i in reversed(range(len(pairs))):
		try:
			key, data = pairs[len(pairs) - i -1]
			tag_dict['%04d'%i] = {
				"count": int(key[:16]),
				"tag": data["p:tag"]
				}
		except Exception as e:
			return str(e)
	return json.dumps(tag_dict)

# given a user name, return all the uids with username matching that pattern
@app.route('/user/<username>')
def names(username):
	return 'User %s' % username


if __name__ == '__main__':
	"Are we in the __main__ scope? Start test server."
	app.run(host='0.0.0.0',port=5000,debug=True)
