#!/bin/bash

# script to push moments from the mira and mrr to epfl ltesrv5 using rsync
# using bandwidth-limited transfer to avoid using all the connection
# and delete moments files for the mrr and mira after they are 10 days old
# ATTENTION: parts of the local and remote paths are hard-written in the rsync command for simplicity, will need changing if the paths change
# Heather Corden 28.3.25

umask 002

SITE='dmc'
REMOTE_USER='lteuser'
REMOTE_HOST='128.178.240.186'
LOCAL_DIR_MIRA='/mom/mira_moments/'
LOCAL_DIR_MRR='/mom/mrr_moments/'

dt=$(date '+%Y/%m/%d %H:%M:%S');

echo "$dt Pushing moments to ltesrv5"

# MIRA moments

rsync -rva --bwlimit=0.5M $LOCAL_DIR_MIRA $REMOTE_USER@$REMOTE_HOST:/awaca/raid/$SITE/mira/data/moments/

# MRR moments

rsync -rva --bwlimit=0.5M $LOCAL_DIR_MRR $REMOTE_USER@$REMOTE_HOST:/awaca/raid/$SITE/mrr/data/moments/


# delete folders older than 10 days to avoid using up too much disk space

DATE10=$(date -d "10 day ago" +"%Y%m%d")
DATE10_SECONDS=$(date -d "${DATE10}" +%s)

# Delete local files older than ten days MRR
find "${LOCAL_DIR_MRR}" -type f | while read -r file; do
  # Extract the date from the file path YYYYMMDD_HHMMSS_moments.nc
  filename=$(basename "${file}")
  file_date_part="${filename:0:8}"
  file_time_part="${filename:9:6}"
  file_datetime="${file_date_part} ${file_time_part:0:2}:${file_time_part:2:2}:${file_time_part:4:2}"
  file_date_seconds=$(date -d "${file_datetime}" +%s 2>/dev/null)

  # Check if the file date is older than ten days
  if [[ -n "${file_date_seconds}" ]] && [[ "${file_date_seconds}" -lt "${DATE10_SECONDS}" ]]; then
    echo "Deleting ${file}"
    rm -f "${file}"
  fi
done

# Delete local files older than ten days MIRA
find "${LOCAL_DIR_MIRA}" -type f | while read -r file; do
  # Extract the date from the file path YYYYMMDD_HHMM_moments
  filename=$(basename "${file}")
  file_date_part="${filename:0:8}"
  file_time_part="${filename:9:4}"
  file_datetime="${file_date_part} ${file_time_part:0:2}:${file_time_part:2:2}:00"
  file_date_seconds=$(date -d "${file_datetime}" +%s 2>/dev/null)

  # Check if the file date is older than ten days
  if [[ -n "${file_date_seconds}" ]] && [[ "${file_date_seconds}" -lt "${DATE10_SECONDS}" ]]; then
    echo "Deleting ${file}"
    rm -f "${file}"
  fi
done

# Delete empty directories
find "${LOCAL_DIR_MRR}" -type d -empty -delete
find "${LOCAL_DIR_MIRA}" -type d -empty -delete

