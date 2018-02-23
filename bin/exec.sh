#!/bin/bash

NAME="proto"
DEST_DIR="/opt/project"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DOCKER="docker"

DOCKER_RUN="$DOCKER run -it --rm -e "uid=`id -u`" -e "ROOT=$DIR/.." -v $DIR/..:$DEST_DIR -v $DIR/../.venv:/root/.local/share/virtualenvs -v /var/run/docker.sock:/var/run/docker.sock ${NAME}_dev"

cd $DIR/.. && make .touch/.dev_dep 1> /dev/null && $DOCKER_RUN bash -c "cd $DEST_DIR && $@"
