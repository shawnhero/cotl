#!/bin/sh
# chkconfig: 123456 90 10
# backgroud process for faking streamed data

start() {
    python stream_generator.py $1 0 > /dev/null 2>&1 &
    echo "stream_generator started."
}
 
stop() {
    pid=`ps -ef | grep '[p]ython stream_generator.py' | awk '{ print $2 }'`
    echo $pid
    kill $pid
    sleep 1
    echo "Server killed."
}
 
if [ "$#" -ne 2 ]; then
    echo "Usage: ./stream_generator.sh {start|stop|restart} {topic_name}"
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
    echo "Usage: ./stream_generator.sh {start|stop|restart}"
    exit 1
esac
exit 0