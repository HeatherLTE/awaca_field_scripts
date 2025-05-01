#!/bin/bash

# script to push mrr data from the ctrl pc to epfl.
# to be used in the case when the mira pc fails
# such that moment files and quicklooks are not created by the mira pc
# Heather Corden 2.4.2025


umask 002

SITE='d47'
REMOTE_USER='lteuser'
REMOTE_HOST='128.178.240.186'
LOCAL_DIR='/home/mrr/data'
REMOTE_DIR="/awaca/raid/${SITE}/mrr/data"


echo "Pushing MRR data to EPFL"


# Get dates for the last two days
DATE1=$(date +"%Y%m%d")         # Today's date
DATE2=$(date -d "1 day ago" +"%Y%m%d") # Yesterday's date
DATE3=$(date -d "2 day ago" +"%Y%m%d")

# Function to sync files for a specific date
# with changing date directory structure
sync_files_for_date() {
  local date=$1
  local year_month="${date:0:6}"
  local year="${date:0:4}"
  local month="${date:4:2}"
  local day="${date:6:2}"
  local remote_path="${REMOTE_DIR}/${year}/${month}/${day}"
  local local_path="${LOCAL_DIR}/${year_month}/${date}"

 
  # Rsync the files with subdirectory creation on the remote side, with bandwidth limit to not use all the connection
  rsync -av --mkpath --bwlimit=0.5M "${local_path}/" "${REMOTE_USER}@${REMOTE_HOST}:${remote_path}/" 
}


# Sync files for the last two days
sync_files_for_date "${DATE1}"
sync_files_for_date "${DATE2}"
sync_files_for_date "${DATE3}"



