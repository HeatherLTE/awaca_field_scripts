#!/bin/bash

# script to push quicklooks from ddu to epfl ltesrv5 using rsync
# ATTENTION: parts of the local and remote paths are hard-written in the rsync command for simplicity, will need changing if the paths change
# Heather Corden 26.3.2025

umask 002

REMOTE_USER='lteuser'
REMOTE_HOST='128.178.240.186'

dt=$(date '+%Y/%m/%d %H:%M:%S');

echo "$dt Pushing quicklooks to ltesrv5"

# WProf quicklooks

rsync -rva /data/awaca/ddu/wprof/quicklooks/ $REMOTE_USER@$REMOTE_HOST:/awaca/ddu/wprof/quicklooks/

# MRR quicklooks

rsync -rva /data/awaca/ddu/mrr/quicklooks/ $REMOTE_USER@$REMOTE_HOST:/awaca/ddu/mrr/quicklooks/

# StXPol 
# should really only tranfser some of the quicklooks

rsync -rva /data/awaca/ddu/stxpol/quicklooks/ $REMOTE_USER@$REMOTE_HOST:/awaca/ddu/stxpol/quicklooks/


