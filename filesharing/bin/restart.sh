#!/bin/sh
#
# Add this file to crontab to start the fastcgi server at boot:
# @reboot /path/to/this/file/restart.sh

PROJDIR="/path/to/project/filesharing"
PIDFILE="$PROJDIR/filesharing.pid"
SOCKET="$PROJDIR/filesharing.sock"
OUTLOG="$PROJDIR/logs/access.log"
ERRLOG="$PROJDIR/logs/error.log"

cd $PROJDIR
if [ -f $PIDFILE ]; then
    kill `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi

python manage.py runfcgi --settings=settings socket=$SOCKET pidfile=$PIDFILE outlog=$OUTLOG errlog=$ERRLOG workdir=$PROJDIR

chmod a+w $SOCKET

