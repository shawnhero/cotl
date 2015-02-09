# this script is supposed to be called only once
# to create the table schemas in HBase
import happybase
import sys

connection = happybase.Connection('c0tl.com')


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
	# for now we store nothing in this table
	# our source of truth about users relies upon the generated id range
}
connection.create_table('users', families)


# user_newsfeed
# rowkey: MD5(uid)+str(timestamp)+MD5(pid)
# col family: p
# col name(fixed, in production one can change it to 'd', 'v'): dump, viewed
# value: photo info dump. easy to access, downside: when modify a photo, not consistent
families = {
	'p': dict(time_to_live=259200)
	# dump, viewed
}
connection.create_table('user_newsfeed', families)



# user_posted_photos
# rowkey: MD5(uid)+str(timestamp)+MD5(pid)
# col family: p
# col name(fixed): dump
# value: photo info dump. easy to access, downside: when modify a photo, not consistent
families = {
	'p': {}
	# dump
}
connection.create_table('user_posted_photos', families)

# user_liked_photos
# rowkey: MD5(uid)+str(timestamp)+MD5(pid)
# col family: p
# col name(fixed): dump
# value: photo info dump. easy to access, downside: when modify a photo, not consistent
families = {
	'p': {}
	# dump
}
connection.create_table('user_liked_photos', families)


# photo information, source of truth for photos
families = {
	'metrics': dict(), # numLiked, numViewed
	'p': dict(max_versions=20), # dump. Preserve version histories
	'likedby': dict()	# dynamic col name: MD5(uid), value: timestamp
	# to be added...
	# 'comments': dict(max_versions=1)

}
connection.create_table('photos', families)


print 'tables created,'
print connection.tables()
