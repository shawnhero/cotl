#!/bin/sh
# chkconfig: 123456 90 10
# backgroud process for faking streamed data

start() {
    python post_photo_consumer.py new_c simple > consumer.log &
    echo "Server started."
}
 
stop() {
    pid=`ps -ef | grep '[p]ython post_photo_consumer.py' | awk '{ print $2 }'`
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
    echo "Usage: ./post_photo_consumer.sh {start|stop|restart}"
    exit 1
esac
exit 0