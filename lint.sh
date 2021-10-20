#!bin/bash

error="\e[1;31m[ERROR]\e[0m"
execution="\e[0;36m[INFO]\e[0m"

echo -e "$execution [...]"

var=$(black analysis/ --diff | grep " " -c)
echo $var

if [ $var -eq 0 ];
then
    echo "$execution All clean!"
else
    black analysis/ --diff
    exit 1
fi

var=$(black models/ --diff | grep " " -c)
echo $var

if [ $var -eq 0 ];
then
    echo "$execution All clean!"
else
    black models/ --diff
    exit 1
fi

var=$(black tests/ --diff | grep " " -c)
echo $var

if [ $var -eq 0 ];
then
    echo "$execution All clean!"
else
    black tests/ --diff
    exit 1
fi

var=$(black back.py --diff | grep " " -c)
echo $var

if [ $var -eq 0 ];
then
    echo "$execution All clean!"
else
    black back.py --diff
    exit 1
fi

var=$(black sendmail.py --diff | grep " " -c)
echo $var

if [ $var -eq 0 ];
then
    echo "$execution All clean!"
else
    black sendmail.py --diff
    exit 1
fi