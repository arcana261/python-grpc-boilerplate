#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

$DIR/exec.sh "pipenv $@"
$DIR/exec.sh 'chown -R $uid:$uid /root/.local/share/virtualenvs && chown $uid:$uid Pipfile.lock'
