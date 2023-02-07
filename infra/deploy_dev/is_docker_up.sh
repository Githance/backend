#!/bin/bash
# Check if docker is up. 
# The user must be in the docker group. 


MAX_TRIES=1200
INTERVAL=1


for (( try=1; try<=$MAX_TRIES; try++ ))
do
  if docker --version &> /dev/null; then
    echo "docker.service is up"
    exit 0
  fi

  if (( $try % 100 == 0 )) || (( $try == 1 )); then
    echo "Try number $try from $MAX_TRIES"
  fi

  sleep $INTERVAL
done

exit 1