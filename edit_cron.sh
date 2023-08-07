#!/bin/ksh

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <keyword>"
    exit 1
fi

keyword=$1

if [[ $keyword == "ALL" ]]; then
    crontab -l | sed 's/^/#/' | crontab -
else
    crontab -l | sed "/$keyword/s/^/#/" | crontab -
fi
### for uncommenting
if [[ $keyword == "ALL" ]]; then
    crontab -l | sed 's/^#//' | crontab -
else
    crontab -l | sed "/$keyword/s/^#//" | crontab -
fi
