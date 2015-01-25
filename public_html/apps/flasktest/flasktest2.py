#!/usr/bin/python

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """<html>
  <h2>Hello from Test Application 2</h2>
</html>"""

@app.route('/<foo>')
def foo(foo):
    return """<html>
  <h2>Test Application 2</2>
  <h3>/%s</h3>
</html>""" % foo

if __name__ == '__main__':
    "Are we in the __main__ scope? Start test server."
    app.run(host='0.0.0.0',port=5000,debug=True)
