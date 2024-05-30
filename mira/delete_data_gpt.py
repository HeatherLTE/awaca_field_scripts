#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 09:58:33 2024

@author: corden
"""

import os
import ftplib
from datetime import datetime, timedelta
from pathlib import Path

# FTP server details
FTP_SERVERS = [
    {'host': 'ftp1.example.com', 'username': 'user1', 'password': 'pass1'},
    {'host': 'ftp2.example.com', 'username': 'user2', 'password': 'pass2'},
]

# Local directory to scan
LOCAL_DIR = '/path/to/local/directory'

# Function to check if file exists on the FTP server
def check_file_on_ftp(ftp_details, file_path):
    try:
        with ftplib.FTP(ftp_details['host']) as ftp:
            ftp.login(ftp_details['username'], ftp_details['password'])
            ftp.cwd(os.path.dirname(file_path))
            file_list = ftp.nlst()
            return os.path.basename(file_path) in file_list
    except ftplib.all_errors as e:
        print(f"FTP error: {e}")
        return False

# Function to check if file exists on any FTP server
def check_file_on_any_ftp(file_path):
    for server in FTP_SERVERS:
        if check_file_on_ftp(server, file_path):
            return True
    return False

# Function to delete old files from local directory
def delete_old_files(directory, days_old=1):
    cutoff_date = datetime.now() - timedelta(days=days_old)
    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = Path(root) / file_name
            file_age = datetime.fromtimestamp(file_path.stat().st_mtime)
            if file_age < cutoff_date and check_file_on_any_ftp(file_path.as_posix()):
                print(f"Deleting file: {file_path}")
                os.remove(file_path)

if __name__ == "__main__":
    delete_old_files(LOCAL_DIR)
