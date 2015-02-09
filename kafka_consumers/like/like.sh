#!/bin/sh
# chkconfig: 123456 90 10
# backgroud process for faking streamed data
# > /dev/null 2>&1
start() {
    echo "topic_name,"$1
    # python post_consume_geoupdate.py $1 &
    # echo "Geo consumer started."
    python like_consume_newsfeed.py $1 &
    echo "Newsfeed consumer started."
    python like_consume_hdfs_dump.py $1 &
    echo "like_consume_hdfs_dump started."
    
}
 
stop() {
    pid=`ps -ef | grep '[p]ython like_consume_newsfeed.py' | awk '{ print $2 }'`
    echo $pid
    kill $pid
    pid=`ps -ef | grep '[p]ython like_consume_hdfs_dump.py' | awk '{ print $2 }'`
    echo $pid
    kill $pid
}

if [ "$#" -ne 2 ]; then
    echo "Usage: bash post.sh {start|stop|restart} {topic_name}"
fi
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