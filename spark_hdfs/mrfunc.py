# 1. define functions to be called in RDD operations
# 2. define how to write to HBase and ElasticSearch to generate views
import json
import happybase
from pyelasticsearch.client import ElasticSearch
# input: raw data delimited by tab
import hashlib

NUM_PHOTO_PER_TAG = 1000
def extractPID(line):
	rawlist = line.split("\t")
	if rawlist[0]=="like":
		t = (1,0)
	else:
		t = (0,1)
	data = {
	"photo": 
		{
			"pid": rawlist[4],
			"location": 
			{
					"latitude": rawlist[5], 
					"longitude": rawlist[6]
			},
			"URL": rawlist[7], 
			"title": rawlist[8],
			"description": rawlist[9],
			"tags": rawlist[10], 
			"timeposted": int(rawlist[11])
		}
	}
	rawdata = json.dumps(data)
	return [rawlist[4], (t, rawdata)]

def countAdd(a, b):
	# a: (t, rawdata)
	t = (a[0][0]+b[0][0], a[0][1]+b[0][1])
	# rawdata will be the same
	return (t, a[1])

#sample input till now:
# (u"102", ((5, 5), "{"photo": {"timeposted": 1422939564, "description": "pdes", "tags": "ptag1,ptag3", "URL": "purl", "title": "ptitle", "pid": "102", "location": {"latitude": "plat", "longitude": "plon"}}}"))
def extractTags(x):
	likes, views = x[1][0][0], x[1][0][1]
	# score = 1.0*likes/(likes+views)
	score = likes
	rawdata = x[1][1]
	parsedrawdata = json.loads(rawdata)
	parsedrawdata["numLiked"] = likes
	parsedrawdata["numViewed"] = views
	tags = parsedrawdata["photo"]["tags"].split(",")
	rawdata = json.dumps(parsedrawdata)
	# construct a dict, to be dumps to a string and added together later
	# eventually it is expected that only 100 top photos will be listed
	# under a certain tag, so we won"t worry about the cell size limit
	# of hbase
	return [[tag, (score, rawdata)] for tag in tags]

def countReorder(x):
	tagcount = 0
	for e in x[1]:
		tagcount += 1
	# tagcount, (tag, [score, rawdata])
	return tagcount, (x[0], x[1] )

def scoreSort(x):
	# tagcount, (tag, (sorted)[score, rawdata])
	scorelist = []
	count = 0
	for y in x[1][1]:
		scorelist.append(y)
		count += 1
	scorelist.sort(reverse=True)
	# make sure we don"t overwhelm users by too many photos under the same tag
	if count > NUM_PHOTO_PER_TAG:
		scorelist = scorelist[:NUM_PHOTO_PER_TAG]
	return x[0], (x[1][0], scorelist)


# sample input
# (2, (u"ptag2", [(0.7692307692307693, "{"photo": {"timeposted": 1422939564, "description": "pdes", "title": "ptitle", "URL": "purl", "tags": "ptag1,ptag2,ptag3", "pid": "101", "location": {"latitude": "plat", "longitude": "plon"}}, "numViewed": 3, "numLiked": 10}"), (0.4230769230769231, "{"photo": {"timeposted": 1422939564, "description": "pdes", "title": "ptitle", "URL": "purl", "tags": "ptag1,ptag2,ptag3", "pid": "103", "location": {"latitude": "plat", "longitude": "plon"}}, "numViewed": 15, "numLiked": 11}")]))

POOL = happybase.ConnectionPool(size=30, host="c0tl.com")
def writeToHBase(x):
	# print "count ", x[0]
	# print "tag name", str(x[1][0])
	# print "first photo", x[1][1][0]
	print "writing to hbase.., cout,", x[0]
	plist = x[1][1]
	pdict = {}
	for i in range(len(plist)):
		pdict[i] = json.loads(plist[i][1])
	with POOL.connection() as connection:
		tagview = connection.table('top_tags')
		rowkey = "%016i"%int(x[0]) + hashlib.md5(str(x[1][0])).digest()
		tagview.put(
			rowkey,
			{
				"p:tag": str(x[1][0]),
				"p:dump": json.dumps(pdict)
			}
		)	

#sample input
# (u"102", ((5, 5), "{"photo": {"timeposted": 1422939564, "description": "pdes", "tags": "ptag1,ptag3", "URL": "purl", "title": "ptitle", "pid": "102", "location": {"latitude": "plat", "longitude": "plon"}}}"))
ES = ElasticSearch("http://localhost:9200")
def saveESDocuments(x):
	print "writing to hbase.., pid,", x[0]
	parsedrawdata = json.loads(x[1][1])
	document = {
		"pid":int(x[0]),
		"likes": x[1][0][0], 
		"views": x[1][0][1],
		"location":{
			"lat":parsedrawdata["photo"]["location"]["latitude"],
			"lon":parsedrawdata["photo"]["location"]["longitude"]
			}
	}
	ES.index('photo_geos', 'photos', document, id=document['pid'])
	# to add