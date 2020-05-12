#!/bin/bash

# Export python path
export PYTHONPATH=${PYTHONPATH}:../

# Start the twitter streamer
python "./twitter/twitter_streamer.py"
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start twitter_streamer: $status"
  exit $status
fi

# Start the reddit streamer
#python "./reddit/reddit_streamer.py"
##status=$?
##if [ $status -ne 0 ]; then
##  echo "Failed to start reddit_streamer: $status"
##  exit $status
##fi