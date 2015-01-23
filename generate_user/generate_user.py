## This is a minimal test
## 1. generate 100 users with uid and geo location
## 2. write the data to hbase
## 3. print the users to command line

import happybase
import random
from struct import *
import numpy as np

def write_user_geo(table, record):
	table.put(record[0], {'Geo:latitude': pack('f',record[1]),
		'Geo:longitude': pack('f',record[2])})

if __name__ == "__main__":
	minLat = 37.383165
	maxLat = 37.500922
	leftLong = -122.442800
	rightLong = -122.192862
	random.seed(2014)
	users = np.empty((100,1), dtype=int)
	userGeos = np.empty((100,2), dtype=float)
	## establish a connection to the table
	connection = happybase.Connection('ec2-54-67-86-242.us-west-1.compute.amazonaws.com')
	table = connection.table('user_location')
	for i in range(100):
		users[i] = i
		para = random.random()
		userGeos[i,0] = para*minLat + (1-para)*maxLat
		para = random.random()
		userGeos[i,1] = para*leftLong + (1-para)*rightLong
		write_user_geo(table, (users[i], userGeos[i,0], userGeos[i,1]))
	# print all the table data
	for key, data in table.scan():
		print unpack('i', key), unpack('f', data['Geo:latitude']), unpack('f', data['Geo:longitude'])
	# close the connection
	np.save('user_geos', np.concatnate((users, userGeos), axis=1))
	connection.close()
