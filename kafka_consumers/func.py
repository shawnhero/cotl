# given uid, pid, timestamp, format and return a rowkey
# sample rowkey: MD5(uid)str(timestamp)MD5(pid)
import time, datetime, sys, hashlib

def get_row_key(uid, pid, timestamp=None, uidfirst=True):
	# expect input: string of int
	uid, pid = str(int(uid)), str(int(pid))
	umd5 = hashlib.md5(uid).digest()
	pmd5 = hashlib.md5(pid).digest()
	if timestamp:
		timestamp = str(timestamp)
		if len(timestamp)!=10:
			raise Exception("Timestamp expected length of 10!")
	else:
		timestamp = str(int(time.time()))
	if uidfirst:
		return umd5+timestamp+pmd5
	else:
		return pmd5+timestamp+umd5

def error_prompt():
	print "Test Usage: [*.py] [uid] [pid] [optional:timestamp]"
	print "Will return MD5(uid)str(timestamp)MD5(pid)"
	sys.exit(0)

if __name__ == '__main__':		
	if len(sys.argv)==3:
		print get_row_key(sys.argv[1], sys.argv[2])
	elif len(sys.argv)==4:
		print get_row_key(sys.argv[1], sys.argv[2], sys.argv[3])
	else:
		error_prompt()