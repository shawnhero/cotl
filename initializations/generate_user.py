import happybase
import random
from struct import *
import numpy as np
from pyelasticsearch.client import ElasticSearch
import sys
sys.path.insert(0, '../elasticsearch')
import hashlib
from es_create import create_es



# Generate random users with random locations
# to do: generate user detailed information and store them in one HBase table
# Usage: see the main function


TESTGEO = [37.803802, -122.467020,37.418149, -121.838739]
class GenerateUsers():
	def __init__(self, minLat=34.820553, maxLat=46.624907, minLong=-120.012679, maxLong=-93.162094, num=100, SMALLTEST=False):
		self.minLat = minLat
		self.maxLat = maxLat
		self.minLong = minLong
		self.maxLong = maxLong
		self.num = num
		if SMALLTEST:
			self.minLat, self.minLong, self.maxLat, self.maxLong = TESTGEO

	# generate random users with random locations
	def generate(self,  seed=2015):
		self.userGeos = np.empty((self.num,3), dtype=float)
		for i in range(self.num):
			self.userGeos[i,0] = i
			para = random.random()
			self.userGeos[i,1] = para*self.minLat + (1-para)*self.maxLat
			para = random.random()
			self.userGeos[i,2] = para*self.minLong + (1-para)*self.maxLong
		np.save('user_geos',  self.userGeos)

	def delete_table(self, connection, table_name):
		## uncomment the following code to prompt check
		# print "Will delete the following tables from HBase:", table_name
		# confirm = raw_input("Sure?(y/n)")
		# if confirm!="y":
		# 	sys.exit(0)
		connection.delete_table(table_name, disable=True)
		print table_name, "deleted."

	# write userGeo information to HBase
	def write_hbase_geo(self, hbase_host='c0tl.com', user_tbl_name="users", geo_tbl_name='user_location'):
		## establish a connection to the table
		try:
			connection = happybase.Connection(hbase_host)
		except Exception as e:
			print "Error while connecting with hbase!"
			sys.exit(0)
		## delete the two table if existed
		tables = connection.tables()
		if user_tbl_name in tables:
			self.delete_table(connection, user_tbl_name)
		if geo_tbl_name in tables:
			self.delete_table(connection, geo_tbl_name)
		## recreate the two tables
		connection.create_table(user_tbl_name, 
			{
			'user_details': dict(max_versions=100)
			# email, phone number, ...
			})
		user_table = connection.table(user_tbl_name)
		print "tables created and connected", user_tbl_name
		
		connection.create_table(geo_tbl_name, 
			{'geo': dict(max_versions=200)
			})
		geo_table = connection.table(geo_tbl_name)
		
		print "tables created and connected", geo_tbl_name

		# write geo data to geo table
		for record in self.userGeos:
			umd5 = hashlib.md5(str(record[0])).digest()
			geo_table.put(umd5, 
				{	'geo:lat': pack('f',record[1]),
					'geo:lon': pack('f',record[2])
				})

		re = geo_table.scan()
		
		print "First result"
		count = 0
		for key, data in re:
			count = count + 1
			if count==1:
				print "sample result found in HBase,"
				print key, unpack('f', data['geo:lat']), unpack('f', data['geo:lon'])
		print 'HBase number of results,', count
		# close the connection
		connection.close()
		

	# write userGeo information to ElasticSearch
	def write_es_geo(self, es_host='http://localhost:9200/', index_name="geos", doc_type='user_geos'):
		# try to connect with ES and delete the index
		es = ElasticSearch('http://localhost:9200/')

		## uncomment the following code to prompt check
		# print "Will delete all the doc in the [index:type] from ElasticSearch:"
		# print index_name, ":", doc_type
		# confirm = raw_input("Sure?(y/n)")
		# if confirm!="y":
		# 	sys.exit(0)


		try:
			create_es()
		except Exception as e:
			print "Error", e
		else:
			print index_name,":", doc_type," deleted!"
		# initializing the documents
		documents = []
		for record in self.userGeos:
			doc = {'uid':int(record[0]), 'location':{'lat':record[1],'lon':record[2]}}
			documents.append(doc)
		print "Bulk indexing", len(documents),"documents.."
		es.bulk_index(index_name, doc_type, documents, id_field='uid')
		es.refresh(index_name)
		# test usage
		print "results from ES,"
		query = {
			"from" : 0, "size" : 2000,
			'query': {
				 "match_all" : { }
			 }
		 }
		res =  es.search(query, index=index_name)
		print len(res['hits']['hits']), "documents found"
		print "sample result"
		print res['hits']['hits'][0]


if __name__ == "__main__":
	if len(sys.argv)==2:
		try:
			num = int(sys.argv[1])
		except ValueError:
			print "Value Error!", sys.argv[1]
			sys.exit(0)
	else:
		print "Useage: [*.py] [number of users]"
		sys.exit(0)
	g = GenerateUsers(num=num)
	g.generate()
	g.write_hbase_geo()
	g.write_es_geo()