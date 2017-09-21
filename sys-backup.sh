#!/bin/bash
# System backup script
# This script id to be run on a remote backup server

PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

rdiff-backup --exclude={"\
/dev/*",\
"/proc/*",\
"/sys/*",\
"/tmp/*",\
"/run/*",\
"/mnt/*",\
"/media/*",\
"/lost+found"\
} ellak::/ /var/backups/ellak
