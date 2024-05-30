#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# a script to send MRR data to the 2 NAS in each OPU
# the files must first bet transferred to eg the MIRA pc, where this script runs
# the script attempts to upload any new or updated files from the radar computer to the NAS
# there is no deletion of files on either computer
# if sync_current_month is True, only attempt to sync the folders for the current month
# if sync_current_month is False, attempt to sync all folders in the data archive path

@author: corden

"""

import ftplib
import os
import datetime
import configparser

# Import config file
config = configparser.ConfigParser()
config.read('/data_movement_scripts/mrr/config_mrr.conf')

sync_current_month = True  # if True, only compare files in the current month to reduce file comparisons

def main():
    # FTP settings
    ftp_user = config['GENERAL']['NAS_ftp_user']
    ftp_password = config['GENERAL']['NAS_ftp_password']
    
    if sync_current_month:
        year_month_string = datetime.datetime.utcnow().strftime("%Y%m")
        
        
        # paths
        local_folder = os.path.join(config['PATHS']['data_archive'], year_month_string)
        remote_folder = os.path.join(config['PATHS']['NAS_archive_path'], year_month_string)
    else:
        # Sync the whole database
        local_folder = config['PATHS']['data_archive']
        remote_folder = config['PATHS']['NAS_archive_path']
    
    # Sync with the NAS database
    mrr_sync_with_nas(ftp_user, ftp_password, local_folder, remote_folder)
    
    if sync_current_month:
        # On the first of each month, also sync the previous month
        # to catch files around midnight of the month change
        if datetime.datetime.utcnow().day == 1:
            yesterday = datetime.datetime.utcnow() - datetime.timedelta(days=1)
            year_month_string = yesterday.strftime("%Y%m")
            
            # paths
            local_folder = os.path.join(config['PATHS']['data_archive'], year_month_string)
            remote_folder = os.path.join(config['PATHS']['NAS_archive_path'], year_month_string)
            
            # Sync with the NAS database
            mrr_sync_with_nas(ftp_user, ftp_password, local_folder, remote_folder)

def mrr_sync_with_nas(ftp_user, ftp_password, local_folder, remote_folder):
    print("----------------------------------------------------------------")
    for nas in ["NAS1", "NAS2"]:
        for network in ["_SW1", "_SW2"]:
            print(f"Uploading MRR data to {nas} on network {network}")
            
            server = config['NETWORK_ADDRESS'][nas + network]
            try:
                # Connect to FTP server
                ftp = ftplib.FTP(server, timeout=10)
                ftp.login(ftp_user, ftp_password)

                # Create list of files to sync
                ftp_files = list_ftp_files(ftp, remote_folder, remote_folder) # the remote folder is passed twice to allow for recursive function calling for subdirectory reading
                local_files = list_local_files(local_folder)
                files_to_sync = list_files_to_sync(ftp_files, local_files)

                # Upload the files to sync
                for file in files_to_sync:
                    local_path = os.path.join(local_folder, file)
                    remote_path = os.path.join(remote_folder, file).replace("\\", "/")
                    ensure_remote_directory_exists(ftp, os.path.dirname(remote_path))
                    with open(local_path, 'rb') as f:
                        ftp.storbinary(f'STOR {os.path.basename(remote_path)}', f)
                        print(f"Uploaded: {file} to {nas}")

                # Close the FTP connection
                ftp.quit()
                print(f" completed sync to {nas} on network {network}")
            except Exception as e:
                print(f" --> FAILED!! {e}")
            else:
                break

def list_ftp_files(ftp, path, remote_root_directory):
    #this function is called recursively to list the contents of of subdirectories on the remote server
    ftp_files = {}
    try:
        ftp.cwd(path)
        #print(f"Changed directory to {path}")
    except ftplib.error_perm:
        #print(f"Failed to change directory to {path}")
        return ftp_files  # Directory does not exist, return empty dictionary
    
    try:
        for item in ftp.mlsd():
            name, metadata = item
            if metadata['type'] == 'file':
                full_path = os.path.join(path, name)
                relative_path = os.path.relpath(full_path, remote_root_directory)
                ftp_files[relative_path] = datetime.datetime.strptime(metadata['modify'], '%Y%m%d%H%M%S')
            elif metadata['type'] == 'dir':
                subdir = os.path.join(path, name)
                ftp_files.update(list_ftp_files(ftp, subdir, remote_root_directory))
    except ftplib.error_perm as e:
        print(f"Error listing directory contents: {e}")
    
    #print(f"Files in {path}: {ftp_files}")
    return ftp_files # a dictionary of relative paths and modification times as datetime.datetime


def list_local_files(path):
    local_files = {}
    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, path)
            local_files[relative_path] = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
    #print(f"Files in local path {path}: {local_files}")
    return local_files # a dictionary of relative paths and modification times as datetime.datetime

def list_files_to_sync(ftp_files, local_files):
    files_to_sync = []
    for file, local_mtime in local_files.items():
        remote_mtime = ftp_files.get(file)
        if not remote_mtime:
            print(f"New file detected: {file}")
            files_to_sync.append(file)
        elif local_mtime > remote_mtime:
            print(f"Updated file detected: {file}")
            print(f"Local time: {local_mtime} > Remote time: {remote_mtime}")
            files_to_sync.append(file)
        #else:
            #print(f"File up-to-date: {file}")
            #print(f"Local time: {local_mtime} <= Remote time: {remote_mtime}")
    return files_to_sync

def ensure_remote_directory_exists(ftp, remote_dir):
    #a convoluted function to check the remote directory exists before sending file
    if not remote_dir:
        return
    if remote_dir.startswith('/'):
        ftp.cwd('/')
    dirs = remote_dir.split('/')
    for dir in dirs:
        if dir:
            try:
                ftp.cwd(dir)
            except ftplib.error_perm:
                try:
                    ftp.mkd(dir)
                    ftp.cwd(dir)
                except ftplib.error_perm as e:
                    print(f"Failed to create directory {dir}: {e}")
                    raise

if __name__ == '__main__':
    main()
