#!/bin/sh
#
# Add this file to crontab to start FutuSMS at boot:
# @reboot /home/futusms/futusms/bin/futusms.sh

PROJDIR="/home/share/futurice_share/futuShareDjango"
PIDFILE="$PROJDIR/futushare.pid"
SOCKET="$PROJDIR/futushare.sock"
OUTLOG="$PROJDIR/logs/access.log"
ERRLOG="$PROJDIR/logs/error.log"

cd $PROJDIR
if [ -f $PIDFILE ]; then
    kill `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi

python manage.py runfcgi --settings=settings socket=$SOCKET pidfile=$PIDFILE outlog=$OUTLOG errlog=$ERRLOG workdir=$PROJDIR

chmod a+w $SOCKET

