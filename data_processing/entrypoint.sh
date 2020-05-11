#!/bin/bash

# Export python path
export PYTHONPATH=${PYTHONPATH}:../

# Start the sentiment analysis server
python "sentiment_analyse.py"
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start data processing: $status"
  exit $status
fi

