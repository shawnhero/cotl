#!/usr/bin/python
from flask import Flask, request, json
import flask
import happybase
hbasehost = 'c0tl.com'
from struct import *
app = Flask(__name__)



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
	try:
		connection = happybase.Connection(hbasehost)
		user_newsfeed = connection.table('user_newsfeed')
		row = user_newsfeed.row(pack('Q',uid),columns=['newsfeed'])
		for key in row.keys():
			# print type(key), type(json.loads(row[key]))
			row[key] = json.loads(row[key])
	except Exception as e:
		print "Exception"
		return str(e)
	print type(row)
	# print row
	return json.dumps(row)

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
