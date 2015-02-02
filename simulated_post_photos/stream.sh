#!/bin/sh
# chkconfig: 123456 90 10
# backgroud process for faking streamed data

start() {
    python stream_generator.py 0 40000 > stream.log&
    echo "stream_generator started."
}
 
stop() {
    pid=`ps -ef | grep '[p]ython stream_generator.py' | awk '{ print $2 }'`
    echo $pid
    kill $pid
    sleep 1
    echo "Server killed."
}
 
case "$1" in
  start)
    start
    ;;
  stop)
    stop   
    ;;
  restart)
    stop
    start
    ;;
  *)
    echo "Usage: ./stream_generator.sh {start|stop|restart}"
    exit 1
esac
exit 0