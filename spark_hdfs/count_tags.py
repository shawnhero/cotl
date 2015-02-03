# usage: $spark/bin/spark-submit [filename]
from operator import add
import sys
from pyspark import SparkConf, SparkContext


def extractTags(line):
	parts = line.split('\t')
	tags = parts[8].split(',')
	del parts[8]
	#newline = '\t'.join(parts)
	return [[t,parts[2]] for t in tags]
def add2(a,b):
	return [a[0]+b[0], a[1]+'\t'+b[1]]
def ispost(line):
	return line.split('\t')[0]=='post'

if __name__=="__main__":
	conf = (SparkConf()
			.setMaster("local")
			.setAppName("My app")
			.set("spark.executor.memory", "1g"))
	sc = SparkContext(conf = conf)
	lines = sc.textFile("/user/photo_dump/20150203_204806.dat")
	result = lines.filter(ispost)\
			.flatMap(extractTags) \
			.map(lambda x: (x[0], [1, x[1]])) \
			.reduceByKey(add2) \
			.map(lambda x: (x[1][0], (x[0],x[1][1]))) \
			.sortByKey(0) # indicates descending sort
	
	output = result.collect()
	for (count, info) in output:
		print count, info
	sc.stop()