# input: raw data delimited by tab
# output: [ tag_timestamp, data ]
def extractTags(line):
	parts = line.split('\t')
	tags = parts[8].split(',')
	# construct a dict, to be dumps to a string and added together later
	# eventually it is expected that only 100 top photos will be listed
	# under a certain tag, so we won't worry about the cell size limit
	# of hbase
	data = {
		"id": parts[2],
		"user_id": parts[1], 
		"location": 
			{
				"latitude": parts[3], 
				"longitude": parts[4]
			},
		"photo": 
			{
				"pid": parts[2],
				"URL": parts[5], 
				"title": parts[6],
				"description": parts[7] , 
				"tags": parts[8], 
				"timeposted": int(parts[9])
			}
	}
	data = json.dumps(data)
	# newline = '\t'.join(parts)
	return [[t,data] for t in tags]

def add2(a,b):
	return [a[0]+b[0], a[1]+'\n'+b[1]]
def ispost(line):
	return line.split('\t')[0]=='post'