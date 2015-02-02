import happybase
import sys
from struct import *

def unpack_photo(rawvalue):
	rawvalue['metrics:numLiked'] = unpack('i',rawvalue['metrics:numLiked'])[0]
	rawvalue['metrics:numViewed'] = unpack('i',rawvalue['metrics:numViewed'])[0]
	rawvalue['details:postby'] = unpack('Q',rawvalue['details:postby'])[0]
	rawvalue['details:born_lat'] = unpack('d',rawvalue['details:born_lat'])[0]
	rawvalue['details:born_lon'] = unpack('d',rawvalue['details:born_lon'])[0]
	rawvalue['details:timeposted'] = unpack('i',rawvalue['details:timeposted'])[0]

if __name__ == "__main__":
	if len(sys.argv)!=2:
		print "Usage: [*.py] [num]"
		sys.exit(0)
	else:
		try:
			num = int(sys.argv[1])
		except ValueError:
			print "Usage: [*.py] [num]"
			sys.exit(0)
	connection = happybase.Connection('c0tl.com')
	to_drop = connection.tables()
	# create the subset table
	if 'photos_sub' in to_drop:
		connection.delete_table('photos_sub', disable=True)
		print 'photos_sub deleted!'
	families = {
		'metrics': dict(max_versions=1),
		# numLiked, numViewed
		'details': dict(max_versions=1),
		# postedBy, comments[], bornGeo, tags, categories
		'likedby': dict(max_versions=1),
		'comments': dict(max_versions=1)

	}
	connection.create_table('photos_sub', families)
	print 'photos_sub created!'
	ptable = connection.table('photos')
	p2table = connection.table('photos_sub')

	for key, data in ptable.scan(limit=num):
		p2table.put(key, data)
	# scan the p2table and print results
	count = 0 
	for key, data in p2table.scan():
		if count ==0:
			unpack_photo(data)
			print unpack('Q', key)[0], data
		count +=1
	print 'total records written,', count
