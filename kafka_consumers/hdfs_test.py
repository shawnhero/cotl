from webhdfs.webhdfs import WebHDFS
import os, tempfile
import time

webhdfs = WebHDFS("c0tl.com", 50070, "hdfs")



# create a temporary file
f = tempfile.NamedTemporaryFile()
f.write(b'Hello world!\n')
f.flush() 

print "Upload file: " + f.name

webhdfs.copyFromLocal(f.name, 
                      "/user/yes.txt")

f.close()