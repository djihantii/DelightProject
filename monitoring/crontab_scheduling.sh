#!/usr/bin/env bash
pathToPythonFile=$PWD
interpreter=/usr/bin/python3.6

crontab -l > /tmp/temp.txt
echo "* * * * *  cd $pathToPythonFile && $interpreter $pathToPythonFile/monotoring.py >> $pathToPythonFile/script_log.log" >> /tmp/temp.txt
crontab /tmp/temp.txt
rm /tmp/temp.txt
