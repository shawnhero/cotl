# this script is supposed to be called only once
# to create the table schemas in HBase
import happybase
import sys

connection = happybase.Connection('ec2-54-67-86-242.us-west-1.compute.amazonaws.com')


# prompt confirm
confirm = raw_input('Will delete all the existing tables and recreate them, are you serious?(y/n)')
if confirm!="y":
	sys.exit(0)
print "deleting all the tables..."

# drop all the tables
to_drop = connection.tables()
for name in to_drop:
	connection.delete_table(name, disable=True)
	print name, 'deleted'
print 'Lists of tables,'
print connection.tables()

families = {
	'user_details': dict(max_versions=100)
	# email, phone number, ...
}
connection.create_table('users', families)


families = {
	'posted_photos': dict(max_versions=1),
	'liked_photos': dict(max_versions=1)
}
connection.create_table('user_photos', families)

families = {
	'metrics': dict(max_versions=1),
	# numLiked, numViewed
	'details': dict(max_versions=1),
	# postedBy, comments[], bornGeo, tags, categories
	'likedby': dict(max_versions=1),
	'comments': dict(max_versions=1)

}
connection.create_table('photos', families)


families = {
	'Geo': dict(max_versions=200)
}
connection.create_table('user_location', families)


families = {
	# set the time to live to be 3 days, i.e.  259200s
	'newsfeed': dict(max_versions=1,time_to_live=259200)
}
connection.create_table('user_newsfeed', families)

print 'tables created,'
print connection.tables()
