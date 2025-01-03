#!/bin/bash

# script to sync recent data from the mrr to the mira pc to make quicklooks
# sync data from today and yesterday and the day before, and delete files older than 30 days


umask 002

REMOTE_USER='mrruser'
REMOTE_HOST='192.168.1.111'
REMOTE_DIR='/U/data/'
LOCAL_DIR='/mom/mrr/'


echo "Fetching recent data from MRR"


# Get dates for the last two days
DATE1=$(date +"%Y%m%d")         # Today's date
DATE2=$(date -d "1 day ago" +"%Y%m%d") # Yesterday's date
DATE3=$(date -d "2 day ago" +"%Y%m%d")
DATE30=$(date -d "30 day ago" +"%Y%m%d")

# Convert dates to seconds since epoch for comparison
DATE1_SECONDS=$(date -d "${DATE1}" +%s)
DATE2_SECONDS=$(date -d "${DATE2}" +%s)
DATE3_SECONDS=$(date -d "${DATE3}" +%s)
DATE30_SECONDS=$(date -d "${DATE30}" +%s)

# Function to sync files for a specific date
sync_files_for_date() {
  local date=$1
  local year_month="${date:0:6}"
  local remote_path="${REMOTE_DIR}/${year_month}/${date}"
  local local_path="${LOCAL_DIR}/${year_month}/${date}"

  # Create local directory structure
  mkdir -p "${local_path}"

  # Rsync the files. Note exclude files starting with . as these are in the process of being written!
  rsync -avz --exclude=".*" "${REMOTE_USER}@${REMOTE_HOST}:${remote_path}/" "${local_path}/"
}

# Delete local files older than ten days
find "${LOCAL_DIR}" -type f | while read -r file; do
  # Extract the date from the file path
  file_date=$(basename "$(dirname "${file}")")
  file_date_seconds=$(date -d "${file_date}" +%s 2>/dev/null)

  # Check if the file date is older than two days
  if [[ -n "${file_date_seconds}" ]] && [[ "${file_date_seconds}" -lt "${DATE30_SECONDS}" ]]; then
    echo "Deleting ${file}"
    rm -f "${file}"
  fi
done

# Delete empty directories
find "${LOCAL_DIR}" -type d -empty -delete

# Sync files for the last two days
sync_files_for_date "${DATE1}"
sync_files_for_date "${DATE2}"
sync_files_for_date "${DATE3}"



