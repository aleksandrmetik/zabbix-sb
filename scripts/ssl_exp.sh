#!/bin/sh
SERVER=$1
PORT=443
TIMEOUT=25
/etc/zabbix/externalscripts/timeout $TIMEOUT /etc/zabbix/externalscripts/ssl-cert-check -s $SERVER -p $PORT -n | awk '{print $6}' | egrep -v "^#|^$"
