#!/bin/sh
# chkconfig: 123456 90 10
# backgroud process for flask

start() {
    python flask_sse.py &
    echo "Server started."
}
 
stop() {
    pid=`ps -ef | grep '[p]ython flask_sse.py' | awk '{ print $2 }'`
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
    echo "Usage: ./flask_sse.sh {start|stop|restart}"
    exit 1
esac
exit 0