#!/bin/sh
# chkconfig: 123456 90 10
# backgroud process for faking streamed data

start() {
    python bg_test.py &
    echo "Server started."
}
 
stop() {
    pid=`ps -ef | grep '[p]ython bg_test.py' | awk '{ print $2 }'`
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
    echo "Usage: ./bg_test.sh {start|stop|restart}"
    exit 1
esac
exit 0