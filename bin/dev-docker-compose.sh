#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

$DIR/docker-compose.sh "-f dev/docker-compose.yml $@"
