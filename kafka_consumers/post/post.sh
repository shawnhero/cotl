#!/bin/sh
# chkconfig: 123456 90 10
# backgroud process for faking streamed data

start() {
    echo "topic_name,"$1
    python consume_geoupdate.py $1 &
    echo "Geo consumer started."
    python consume_newsfeed.py $1 &
    echo "Newsfeed consumer started."
    python consume_photos.py $1 &
    echo "Photo consumer started."
    python consume_userphoto.py $1 &
    echo "UserPhoto consumer started."
    python consume_hdfs_dump.py $1 &
    # python consume_hdfs_dump.py new_e > /dev/null &
    
}
 
stop() {
    pid=`ps -ef | grep '[p]ython consume_geoupdate.py' | awk '{ print $2 }'`
    echo $pid
    kill $pid
    pid=`ps -ef | grep '[p]ython consume_newsfeed.py' | awk '{ print $2 }'`
    echo $pid
    kill $pid
    pid=`ps -ef | grep '[p]ython consume_photos.py' | awk '{ print $2 }'`
    echo $pid
    kill $pid
    pid=`ps -ef | grep '[p]ython consume_userphoto.py' | awk '{ print $2 }'`
    echo $pid
    kill $pid
    pid=`ps -ef | grep '[p]ython consume_hdfs_dump.py' | awk '{ print $2 }'`
    echo $pid
    kill $pid
}
 
case "$1" in
  start)
    start $2
    ;;
  stop)
    stop   
    ;;
  restart)
    stop
    start $2
    ;;
  *)
    echo "Usage: bash post.sh {start|stop|restart} {topic_name}"
    exit 1
esac
exit 0