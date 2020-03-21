#!/bin/bash

# Processes to start
#report_ip_script="./cronjob/report_ip.py"
sentiment_server_script="./sentiment/vader_sentiment.py"

# Export python path
export PYTHONPATH=${PYTHONPATH}:../

# Start the report_ip process
#python $report_ip_script &
#status=$?
#if [ $status -ne 0 ]; then
#  echo "Failed to start cronjob: report_ip: $status"
#  exit $status
#fi

# Start the sentiment analysis server
python $sentiment_server_script
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start sentiment analysis server: $status"
  exit $status
fi

# Naive check runs checks once a minute to see if either of the processes exited.
# This illustrates part of the heavy lifting you need to do if you want to run
# more than one service in a container. The container exits with an error
# if it detects that either of the processes has exited.
# Otherwise it loops forever, waking up every 60 seconds

#while sleep 60; do
#  ps aux |grep report_ip.py |grep -q -v grep
#  PROCESS_1_STATUS=$?
#  ps aux |grep my_second_process |grep -q -v grep
#  PROCESS_2_STATUS=$?
#  # If the greps above find anything, they exit with 0 status
#  # If they are not both 0, then something is wrong
#  if [ $PROCESS_1_STATUS -ne 0 -o $PROCESS_2_STATUS -ne 0 ]; then
#    echo "One of the processes has already exited."
#    exit 1
#  fi
#done