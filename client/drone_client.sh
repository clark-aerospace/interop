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

# Tests the images.
if [ "$1" == "test" ]
then
    docker run --net="host" -it auvsisuas/interop-client bash -c \
        "export PYTHONPATH=/interop/client && \
         cd /interop/client && \
         source venv37/bin/activate && \
		 ./tools/drone_cli.py --url udp://:14540 load_mission --mission_id 1 --interop_url http://127.0.0.1:8000 --interop_username testuser --interop_password testpass && \
		 deactivate"
fi
