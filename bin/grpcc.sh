#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

CONTAINER_NAME=$($DIR/dev-docker-compose.sh "ps | grep grpcc | sed 's/\\s.*//g'")
CONTAINER_NAME_NO_WHITESPACE="$(echo -e "${CONTAINER_NAME}" | tr -d '[:space:]')"
DOCKER="docker"

$DOCKER exec -it "$CONTAINER_NAME_NO_WHITESPACE" grpcc $@
