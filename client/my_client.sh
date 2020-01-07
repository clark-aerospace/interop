#!/bin/bash
# Utility script

CLIENT=$(dirname ${BASH_SOURCE[0]})
REPO=${CLIENT}/..

# Quit on any error.
set -e

# Run commands from context of client directory.
cd $CLIENT

#build the docker image
if [ "$1" == "build" ]
then
	docker build -t my_interop .
fi

#run the docker container with an interactive shell in a virtuall environment
if [ "$1" == "run" ]
then 
	docker run --net=host --interactive --tty my_interop
fi
