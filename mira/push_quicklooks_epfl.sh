#!/bin/bash

# script to push quicklooks from the mira to epfl ltesrv5 using rsync
# since the reverse tunnel does not stay reliably open to pull the quicklooks from the epfl side
# ATTENTION: parts of the local and remote paths are hard-written in the rsync command for simplicity, will need changing if the paths change
# Heather Corden 28.1.2025

umask 002

SITE='d85'
REMOTE_USER='lteuser'
REMOTE_HOST='128.178.240.186'

dt=$(date '+%Y/%m/%d %H:%M:%S');

echo "$dt Pushing quicklooks to ltesrv5"

# MIRA quicklooks

rsync -rva /home/data/awaca_scriptsnlogs/quicklook_plots/mira/ $REMOTE_USER@$REMOTE_HOST:/awaca/raid/$SITE/mira/quicklooks/

# MRR quicklooks

rsync -rva /home/data/awaca_scriptsnlogs/quicklook_plots/mrr/ $REMOTE_USER@$REMOTE_HOST:/awaca/raid/$SITE/mrr/quicklooks/

