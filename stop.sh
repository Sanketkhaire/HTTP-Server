#!/bin/bash

#reference : https://stackoverflow.com/a/14669525

pid=`ps -ef | grep "main.py" | awk '{print $2}' | head -1`
kill $pid
echo "myHTTP server is stopped"