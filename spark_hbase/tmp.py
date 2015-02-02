import happybase
import sys
from struct import *



if __name__ == "__main__":
	connection = happybase.Connection('c0tl.com')
	to_drop = connection.tables()
	# create the subset table
	if 'photos_tmp' in to_drop:
		connection.delete_table('photos_tmp', disable=True)
		print 'photos_tmp deleted!'
	families = {
		'metrics': dict(max_versions=1),
		# numLiked, numViewed
		'details': dict(max_versions=1),
		# postedBy, comments[], bornGeo, tags, categories
		'likedby': dict(max_versions=1),
		'comments': dict(max_versions=1)

	}
	connection.create_table('photos_tmp', families)
	print 'photos_tmp created!'