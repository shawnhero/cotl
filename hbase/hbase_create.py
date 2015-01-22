import happybase

connection = happybase.Connection('ec2-54-67-86-242.us-west-1.compute.amazonaws.com')

families = {
	'user_details': dict(max_versions=100)
	# email, phone number, ...
}
connection.create_table('users', families)

families = {
	'metrics': dict(max_versions=200)
	## numLikes, numBeLiked
}
connection.create_table('user_metrics', families)

families = {
	'posted_photos': dict(max_versions=1),
	'liked_photos': dict(max_versions=1)
}
connection.create_table('user_photos', families)

families = {
	'photo_details': dict(max_versions=1)
	# takenBy, bornGeo, addrS3, tags, categories
}
connection.create_table('photos', families)

families = {
	'metrics': dict(max_versions=200)
	## numLikes, numBeLiked
}
connection.create_table('photo_metrics', families)

families = {
	'Geo': dict(max_versions=200)
}
connection.create_table('user_location', families)


families = {
	'newsfeed': dict(max_versions=1)
}
connection.create_table('user_newsfeed', families)

print connection.tables()
