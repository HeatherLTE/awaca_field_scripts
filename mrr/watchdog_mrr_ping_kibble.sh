#!/bin/bash

# a script to check the mrr is reachable and if so make a kibble on the control pc

umask 002

IPMRR='192.168.1.150'
PATH_KIBBLE='/home/mrr/watchdog/kibble_mrr.txt'


#!/bin/bash

# Define the remote computer's IP address or hostname
REMOTE_HOST="192.168.1.100"

# Try to ping the remote computer
if ping -c 1 "$IPMRR" &> /dev/null
then
    # If ping is successful, get the current date and time
    CURRENT_DATE_TIME=$(date)
    
    # Write the current date and time to the text file, overwriting it
    echo "$CURRENT_DATE_TIME" > "$PATH_KIBBLE"
    
    # Optional: Print a success message
    echo "Ping to mrr successful. Date and time saved to $FILE_PATH"
else
    # Optional: Print a failure message
    echo "Ping failed. Remote computer is not accessible."
fi

