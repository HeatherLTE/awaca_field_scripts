#!/bin/bash

# a very very basic script for fetching data from the mrr to the mira via rsync
# note it syncs the directory, which is probably not a good idea

umask 002

IPMRR='192.168.1.150'
path_remote='/U/data/'
path_local='/m2data/mrr/'


echo "Fetching data from MRR"

rsync -rva mrruser@$IPMRR:$path_remote $path_local

#rsync -rva mrruser@192.168.1.150:/U/data/ /m2data/mrr/
