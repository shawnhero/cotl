# usage: $spark/bin/spark-submit [filename]
from operator import add
import sys, json
from pyspark import SparkConf, SparkContext
import time, datetime
import happybase
from mrfunc import *

def create_new_tag_table_product_version():
	# create new table view with name including a timestamp
	try:
		connection = happybase.Connection('c0tl.com')
		# rowkey: [000count][MD5(tagname)]
		families = {
			'p': dict(max_versions=1)
			# col qualifier: 'dump'
			# value: json dump of photo info, delimited by '\n'
			# Worst case: 100Byte*1000=100KB, sound good
		}
		new_name = "toptags_"+datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M')
		connection.create_table(new_name, families)
		# write the table name to file
		with open('view_table_name', 'a') as f:
			f.write('\n'+new_name)
		print "table created!", new_name
	except Exception as e:
		print str(e)
		sys.exit(0)
	return new_name


def create_new_tag_table(hbase_host='c0tl.com', hbasetblname='top_tags'):
	try:
		connection = happybase.Connection(hbase_host)
	except Exception as e:
		print "Error while connecting with hbase!"
		sys.exit(0)
	## delete the two table if existed
	tables = connection.tables()
	if hbasetblname in tables:
		connection.delete_table(hbasetblname, disable=True)
		print hbasetblname, 'deleted!'
	
	## recreate the two tables
	connection.create_table(hbasetblname, {'p': {}})
	print hbasetblname, "table created!"

def create_new_es_table():
	es = ElasticSearch("http://localhost:9200")
	mapping = {
		 'photos': {
			'properties': {
				'pid': {'type': 'long'},
				'likes': {'type': 'long'},
				'views': {'type': 'long'},
				'location': {'type': 'geo_point'}
			},
			"_id" : {
				"path" : "pid"
			}
		}
	}
	## create index
	try:
		es.delete_index('photo_geos')
		print "Index 'photo_geos' deleted!"
	except Exception as e:
		pass
	es.create_index('photo_geos', settings={'mappings': mapping})
	print "Index 'photo_geos' created!"
	es.refresh('photo_geos')
	# create es table
	# photolat, photolon, photoscore

# return the file prefixes in the recent 3 days
	# if the current time is 2015-02-03, 14:27
	# sample output
	#['20150203','20150202','20150201','20150131_14','20150131_15',
	# '20150131_16','20150131_17','20150131_18','20150131_19',
	# '20150131_20','20150131_21','20150131_22','20150131_23']
def files_to_read():
	now = int(time.time())
	day3 = now - 3*24*3600
	day2 = now - 2*24*3600
	day1 = now - 1*24*3600
	prefix0 = datetime.datetime.fromtimestamp(now).strftime('%Y%m%d')
	prefix1 = datetime.datetime.fromtimestamp(day1).strftime('%Y%m%d')
	prefix2 = datetime.datetime.fromtimestamp(day2).strftime('%Y%m%d')
	prefix3 = datetime.datetime.fromtimestamp(day3).strftime('%Y%m%d_%H')
	filelist = [prefix0, prefix1, prefix2, prefix3]
	current, end3 = prefix3, prefix3[:-2] +'23'
	while current <= end3:
		filelist.append(current)
		current = current[:-2] + str(int(current[-2:])+1)
	return filelist
	
def files_to_read_tmp():
	# only return today's file prefixes
	now = int(time.time())
	prefix0 = datetime.datetime.fromtimestamp(now).strftime('%Y%m%d')
	return [prefix0]
	
if __name__=="__main__":

	conf = (SparkConf()
			.setMaster("local")
			.setAppName("MRJOB")
			.set("spark.executor.memory", "4g"))
	sc = SparkContext(conf = conf)

	hbasetblname='top_tags'
	esindexname = 'photo_geos'
	esdocname = 'photos'
	# create_new_tag_table()
	# create_new_es_table()


	# gv = Generate_Views(hbasetblname='top_tags',esindexname='photo_geos', esdocname='photos')
	print "Reading the files"
	lines = sc.textFile("/user/photo_dump/like/20150208_084933.dat")


	result = lines.filter(lambda x: x[:4]=="like" or x[:4]=="view")\
			.map(extractPID) \
			.reduceByKey(countAdd)
	# sample element in the dataset
	# (u'102', ((5, 5), '{"photo": {"timeposted": 1422939564, "description": "pdes", "tags": "ptag1,ptag3", "URL": "purl", "title": "ptitle", "pid": "102", "location": {"latitude": "plat", "longitude": "plon"}}}'))

	# now we are ready to update to the elastic seach
	# 
	result.foreach(saveESDocuments)
	# print(len(gv.documents))
	# now we continue to summarize the tag information
	# [tag, (score, rawdata) for tag in tags]

	tag_result = result.flatMap(extractTags) \
			.groupByKey() \
			.map(countReorder) \
			.sortByKey(0) \
			.zipWithIndex().filter(lambda x: x[1]<1000) \
			.map(lambda x: x[0]) \
			.map(scoreSort)
	tag_result.foreach(writeToHBase)
	sc.stop()
