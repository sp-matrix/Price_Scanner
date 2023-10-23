#!/bin/ksh

# Path to your log file
LOG_FILE="/path/to/your/logfile.log"

# Get the current date and time
NOW=$(date +%s)

# Check for errors in the last 15 minutes
FIFTEEN_MINUTES_AGO=$(date -d"15 minutes ago" +%s)

awk -v start=$FIFTEEN_MINUTES_AGO -v now=$NOW '
BEGIN { FS=" "; }
{
    # Convert log timestamp to epoch time
    "date -d\""$1" "$2"\" +%s" | getline log_time

    # Check if log_time is within the last 15 minutes and if the line contains "ERROR"
    if (log_time >= start && log_time <= now && $0 ~ /ERROR/)
        print "Error found: " $0
}' $LOG_FILE

# Check if the log file has been updated in the last 20 minutes
TWENTY_MINUTES_AGO=$(date -d"20 minutes ago" +%s)

if [[ $(stat -c %Y $LOG_FILE) -le $TWENTY_MINUTES_AGO ]]; then
    echo "The log file has not been updated in the last 20 minutes."
else
    echo "The log file has been updated in the last 20 minutes."
fi
