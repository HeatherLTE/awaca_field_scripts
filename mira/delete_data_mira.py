#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# a script to safely delete data from the mira which has been stored on at least one NAS
# login to each NAS (via both networks)
# for each locally stored file on the mira pc,
#   check whether the file is stored on at least one nas 
#   and is older than n days
#   if so delete from mira pc


@author: corden

"""

import ftplib
import os
import datetime
import configparser

# Import config file
config = configparser.ConfigParser()
config.read('/data_movement_scripts/config.conf')

days_old = 60
cutoff_date = datetime.datetime.utcnow() - datetime.timedelta(days=days_old)


def main():
    # FTP settings
    ftp_user = config['GENERAL']['NAS_ftp_user']
    ftp_password = config['GENERAL']['NAS_ftp_password']
    
    
    local_folder = config['PATHS']['data_archive']
    remote_folder = config['PATHS']['NAS_archive_path']
    
    # list local files
    local_files = list_local_files(local_folder)
    
    for file, local_mtime in local_files.items():
        if file_on_any_nas(file, remote_folder, ftp_user, ftp_password ):
            if local_mtime < cutoff_date:
                print(f"removing {file} as it is on at least one NAS and is older than {days_old} days old")
                os.remove(os.path.join(local_folder, file))
                
    #delete empty directories on the local folder
    delete_empty_folders(local_folder)
    
#--------------------------------------------------------------------------------
                
# Function to check if file exists on any FTP server
def file_on_any_nas(local_file_relative_path, remote_folder, ftp_user, ftp_password):
    for nas in ["NAS1", "NAS2"]:
        if check_file_on_ftp(nas, local_file_relative_path, remote_folder, ftp_user, ftp_password):
            return True
    return False

# Function to check if file exists on the FTP server
def check_file_on_ftp(nas, local_file_relative_path, remote_folder, ftp_user, ftp_password):
    
    for network in ["_SW1", "_SW2"]:
        server = config['NETWORK_ADDRESS'][nas + network]
        
        # Connect to FTP server
        try:
            ftp = ftplib.FTP(server, timeout=20)
            ftp.login(ftp_user, ftp_password)
            
            # to check if a file exists we have to list all the files...
            # to make it faster, first navigate to the subfolder where the file is expected to be
            subfolder_path = os.path.dirname(local_file_relative_path)
            #print(subfolder_path)
            remote_subfolder = os.path.join(remote_folder, subfolder_path)
            #print(remote_subfolder)
            ftp_files = list_ftp_files(ftp, remote_subfolder, remote_folder) # the remote folder is passed twice to allow for recursive function calling for subdirectory reading
            #print(ftp_files)
            ftp.quit()
            
            if local_file_relative_path in ftp_files:
                #print(f"{local_file_relative_path} found on {nas}")
                return True
            else:
                #print(f"{local_file_relative_path} not found on {nas}")
                return False
            
        except Exception as e:
            print(f"FTP Error {e}")
            continue
    
    #return false if both networks tried and files not found
    return False
         
#function to list contents of only current folder on ftp server
def list_ftp_files(ftp, path, remote_root_directory):

    ftp_files = {}
    try:
        ftp.cwd(path)
        #print(f"Changed directory to {path}")
        #ftp.pwd()
    except ftplib.error_perm as e:
        #ftp.pwd()
        #print(f"Failed to change directory to {path} {e}")
        return ftp_files  # Directory does not exist, return empty dictionary    
    try:
        for item in ftp.mlsd():
            name, metadata = item
            if metadata['type'] == 'file':
                full_path = os.path.join(path, name)
                relative_path = os.path.relpath(full_path, remote_root_directory)
                ftp_files[relative_path] = datetime.datetime.strptime(metadata['modify'], '%Y%m%d%H%M%S')              
    except ftplib.error_perm as e:
        print(f"Error listing directory contents: {e}")
    
    #print(f"Files in {path}: {ftp_files}")
    return ftp_files # a dictionary of relative paths (relative to remote_root_directory) and remote modification times


# function to list local files and modification times
def list_local_files(path):
    local_files = {}
    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, path)
            local_files[relative_path] = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
    #print(f"Files in local path {path}: {local_files}")
    return local_files # a dictionary of relative paths and modification times as datetime.datetime


#delete empty folders (eg empty day folders once all files deleted, empty month folders once all days deleted)
def delete_empty_folders(path):
    """
    Recursively delete empty folders in the directory structure.
    :param path: The root directory to start checking for empty folders.
    :return: True if the directory is empty and deleted, False otherwise.
    """
    # Check if the path exists and is a directory
    if not os.path.isdir(path):
        return False
    
    # Get the list of all entries (files and directories) in the current directory
    entries = os.listdir(path)
    
    # Recursively delete empty subdirectories
    for entry in entries:
        entry_path = os.path.join(path, entry)
        if os.path.isdir(entry_path):
            # Recursively check the subdirectory
            delete_empty_folders(entry_path)
    
    # Get the list of entries again after deleting empty subdirectories
    entries = os.listdir(path)
    
    # If the directory is empty, delete it
    if not entries:
        os.rmdir(path)
        print(f"Deleted empty folder: {path}")
        return True
    else:
        return False



if __name__ == '__main__':
    main()
