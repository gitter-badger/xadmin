#!/bin/sh
NAME="xadmin4"
if [ ! -n "$NAME" ];then
    echo "no arguments"
    exit;
fi

echo $NAME
ID=`ps -ef | grep "$NAME" | grep -v "$0" | grep -v "grep" | awk '{print $2}'`
echo $ID
echo "################################################"
for id in $ID
do
kill -9 $id
echo "kill $id"
done
echo  "################################################"
uwsgi --ini /www/web/xadmin4/demo_app/demo/script/uwsgi.ini
chmod 777 /www/web/xadmin4/demo_app/script/uwsgi.sock
