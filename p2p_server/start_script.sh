#!/bin/sh

case "$1" in
    start)
        kill -9 `cat /var/www/p2p_server/service.pid`
        python3 /var/www/p2p_server/curl_server.py &
    ;;
    stop)
        kill -9 `cat /var/www/p2p_server/service.pid`
    ;;

esac

exit 0
