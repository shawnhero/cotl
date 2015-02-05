# usage: $spark/bin/spark-submit [filename]
from operator import add
import sys, json
from pyspark import SparkConf, SparkContext
import time, datetime
import happybase


def create_hbase_view(lists, hbasehost, table_name):
	connection = happybase.Connection(hbasehost)
	tbl = connection.table(table_name)
	for photo in lists:
		# [rowkey, [rowkey, col_family, col_qualifier, value] ]
		tbl.put(
			photo[0],
			{
				photo[1][1]+":"+photo[1][2]:photo[1][3]
			})

def create_new_tag_table():
	# create new table view with name including a timestamp
	try:
		connection = happybase.Connection('c0tl.com')
		families = {
			'photos': dict(max_versions=1)
			# col qualifier: pid
			# value: json dump of photo info
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

# return the file prefixes in the recent 3 days
	# if the current time is 2015-02-03, 14:27
	# sample output
	#['20150203',
	# '20150202',
	# '20150201',
	# '20150131_14',
	# '20150131_15',
	# '20150131_16',
	# '20150131_17',
	# '20150131_18',
	# '20150131_19',
	# '20150131_20',
	# '20150131_21',
	# '20150131_22',
	# '20150131_23']
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
	
	
def flat_row(line):
	# expected input [(count, (tag, data), index]
	# expected output
	# [rowkey, [rowkey, col_family, col_qualifier, value] ]
	rowkey = str(line[0][0]) + "\t" + line[0][1][0]
	col_family = 'photos'
	col_qualifier = 'photolist'
	photolist = line[0][1][1]
	return [rowkey, [rowkey, col_family, col_qualifier, photolist] ]

if __name__=="__main__":
	conf = (SparkConf()
			.setMaster("local")
			.setAppName("MRJOB")
			.set("spark.executor.memory", "1g"))
	sc = SparkContext(conf = conf)
	files = ','.join(["/user/photo_dump/"+f+"*" for f in files_to_read_tmp()])
	print "Reading the files"
	lines = sc.textFile("/user/photo_dump/20150203_220005.dat")
	result = lines.filter(isbehavior)\
			.flatMap(extractTags) \
			.map(lambda x: [x[0], [1, x[1]] ]) \
			.reduceByKey(add2) \
			.map(lambda x: [x[1][0], (x[0],x[1][1]) ]  ) \
			.sortByKey(1) \
			.zipWithIndex().filter(lambda x: x[1]<100) \
			.map(flat_row)
	table_name = create_new_tag_table()
	create_hbase_view(result.collect(), "c0tl.com", table_name)
