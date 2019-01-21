#!/bin/bash
lockdir1=/tmp/.myscript.lock1
lockdir2=/tmp/.myscript.lock2

if mkdir "$lockdir1" 2> /dev/null
then
    rm -r "$lockdir1"
    echo $(($1 * 2))
    exit
elif mkdir "$lockdir2" 2> /dev/null
then
    echo $(($1 * 2))
    rm -r "$lockdir2"
    exit
else
    echo "Error"
    rm -r "$lockdir1"
    rm -r "$lockdir2"
    pkill calc.sh
    exit
fi
