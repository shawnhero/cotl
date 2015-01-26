# author: oskar.blom@gmail.com
#
# Make sure your gevent version is >= 1.0
import gevent
from gevent.wsgi import WSGIServer
from gevent.queue import Queue

from flask import Flask, Response

import time
import numpy as np


# SSE "protocol" is described here: http://mzl.la/UPFyxY
class ServerSentEvent(object):

	def __init__(self, data):
		self.data = data
		self.event = None
		self.id = None
		self.desc_map = {
				self.data : "data",
				self.event : "event",
				self.id : "id"
		}

	def encode(self):
		if not self.data:
				return ""
		lines = ["%s: %s" % (v, k) 
						 for k, v in self.desc_map.iteritems() if k]
		
		return "%s\n\n" % "\n".join(lines)

app = Flask(__name__,static_folder='static', static_url_path='')
subscriptions = []

@app.route('/')
def root():
	return app.send_static_file('index.html')


# url_for('static', filename='point_listener.js')
# Client code consumes like this.
@app.route("/stream")
def index():
	debug_template = """
		 <html>
			 <head>
			 </head>
			 <body>
				 <h1>Server sent events</h1>
				 <div id="event"></div>
				 <script type="text/javascript">
				 var eventOutputContainer = document.getElementById("event");
var evtSrc = new EventSource("/subscribe");
evtSrc.onmessage = function(e) {
		console.log(e.data);
		eventOutputContainer.innerHTML = e.data;
};
				 </script>
			 </body>
		 </html>
		"""
	return(debug_template)

@app.route("/debug")
def debug():
	return "Currently %d subscriptions" % len(subscriptions)

@app.route('/<path:filename>')
def send_foo(filename):
	return send_from_directory('../../http/', filename)

@app.route("/publish")
def publish():
	#Dummy data - pick up from request for real data
	def notify():
		# msg = str(time.time())
		msg = "random number: "+str(np.random.randint(0,100))
		for sub in subscriptions[:]:
			sub.put(msg)
	gevent.spawn(notify)
	
	return "OK"

@app.route("/subscribe")
def subscribe():
	def gen():
		q = Queue()
		subscriptions.append(q)
		try:
			# while True:
			end = time.time() + 60
			while time.time() < end:
				result = q.get()
				print "result", result
				ev = ServerSentEvent(str(result))
				yield ev.encode()
				sleep(0.3)
				# Keep connection alive no more then... (s)
		except GeneratorExit: # Or maybe use flask signals
			subscriptions.remove(q)

	return Response(gen(), mimetype="text/event-stream")

@app.route('/stream')
def stream():
	return Response(event_stream(),mimetype="text/event-stream")

if __name__ == "__main__":
	app.debug = False
	server = WSGIServer(("", 5001), app)
	server.serve_forever()
	# app.run(host='0.0.0.0',port=5001,debug=True)
	# Then visit http://localhost:5000 to subscribe 
	# and send messages by visiting http://localhost:5000/publish