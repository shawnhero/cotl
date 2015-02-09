#!/usr/bin/python
from flask import Flask, request, json
import flask
import happybase
import hashlib
hbasehost = 'c0tl.com'
from struct import *
app = Flask(__name__)

#retrieve all the photos
def get_row_prefix(uid, timestamp=None):
	prefix = hashlib.md5(str(uid)).digest()
	if timestamp:
		prefix += str(timestamp)
	print "Prefix:",prefix
	return prefix
	

# APIs offered by flask

@app.route('/')
def home():
	return """<html>
  <h2>Welcome to the colt API!</h2>
</html>"""

# given a user id, return the newsfeed
@app.route('/uid/<userid>')
def newsfeed(userid):
	# return userid
	try:
		uid = int(userid)
	except ValueError:
		return "Invalid uid"
	# connect to HBase and return the newsfeed
	alldata = {}
	try:
		connection = happybase.Connection(hbasehost)
		user_newsfeed = connection.table('user_newsfeed')
		count = 0
		for key, data in user_newsfeed.scan(row_prefix=get_row_prefix(userid)):
			# skip those viewed photos
			if 'p:viewed' in data:
				continue
			alldata[count] = json.loads(data["p:dump"])
			count +=1
	except Exception as e:
		print "Exception"
		return str(e)
	# print row
	# doing the following will be better than json.loads once every time
	# return str(json.dumps(alldata).replace('\\',''))
	return json.dumps(alldata)


# return the distribution of the number of newsfeed
@app.route('/dist')
def dist_newsfeed():
	return 0


# given a location, return the most popular photos
@app.route('/location/<geo>')
def location(foo):
	return 0

# given a hashtag, return the photos linked with that
@app.route('/hashtag/<tag>')
def tag(foo):
	return 0

# given a photo id, return the detailed information


# return the most popular hashtags
@app.route('/trending_hashtags')
def trending_hashtags(foo):
	return 0

# given a user name, return all the uids with username matching that pattern
@app.route('/user/<username>')
def names(username):
	return 'User %s' % username


if __name__ == '__main__':
	"Are we in the __main__ scope? Start test server."
	app.run(host='0.0.0.0',port=5000,debug=True)
