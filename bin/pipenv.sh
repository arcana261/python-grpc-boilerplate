#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

$DIR/exec.sh "ENV=dev pipenv $@"
$DIR/exec.sh 'chown -R $uid:$uid /root/.local/share/virtualenvs && chown $uid:$uid Pipfile.lock'
