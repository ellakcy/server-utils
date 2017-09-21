#!/bin/bash
# Container backup for ellak.org.cy server
# This script is to be run locally on the docker host

BACKUP_DIR=/var/backups/docker
CONTAINERS=$(docker ps | grep -v CONTAINER | awk '{print $1}')

for CONT in $CONTAINERS
do
    NAME=$(docker inspect $CONT | grep -m1 Name | cut -d\" -f4 | tr -d '/')
    docker export $CONT -o $BACKUP_DIR/$NAME-img.tar
done
