#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 10:10:54 2024

@author: corden
"""
# a script that creates a local file containing the date and attempts to sync it to the two control pcs
# adapted from the awacasurf local watchdog written by Felipe
# this script should be exectuted every half hour by crontab

import datetime as dt
import ftplib
import configparser
import os

# load config file
config = configparser.ConfigParser()
config.read('/home/data/awaca_scriptsnlogs/scripts/config.conf')


def main():
    # ftp settings
    ftp_user = config['GENERAL']['PCCONTROL_ftp_user']
    ftp_password = config['GENERAL']['PCCONTROL_ftp_password']

    # write in the home folder of the control PC
    local_folder = config['PATHS']['local_watchdog_path']
    local_file_path = os.path.join(local_folder, 'kibble_mirapc.txt')
    remote_folder = config['PATHS']['ctrlpc_watchdog_path']
    remote_file_path = os.path.join(remote_folder, 'kibble_mirapc.txt')

    # create a local watchdog file with current time to copy in the remote Control PCs
    create_local_watchdog_file(local_file_path)
    update_remote_watchdog( ftp_user, ftp_password, local_file_path, remote_file_path)
    

##############################################################################
def create_local_watchdog_file(local_file_path):
    """
    Create a local text file with the date

    Parameters
    ----------
    local_file_path : str
        full path to the file to be created, including file name
    """
    # Get the current timestamp in utc
    timestamp = dt.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        with open(local_file_path, 'w') as file:
            file.write(timestamp)
        print(f"Updated local watchdog file with timestamp '{timestamp}'")
    
    except Exception as e:
        print(f'An error occurred when creating the local watchdog file: {e}')


            
def update_remote_watchdog(ftp_user, ftp_password, local_file_path, remote_file_path):
    """
    Sends the watchdog kibble file to both control pcs.
    Using both networks if required

    Parameters
    ----------
    ftp_user : str
    ftp_password : str
    local_file_path : str
        full path to the local watchdog file, with the filename
    remote_file_path : str
        full path to the remote watchdog file, with the filename
    """

    for pc in ["PCCONTROL1", "PCCONTROL2"]:
        for network in ["_SW1", "_SW2"]:
            print(f"Uploading local watchdog to {pc} on network {network}")
            
            server = config['NETWORK_ADDRESS'][pc + network]
            try:
                # Connect to FTP server
                ftp = ftplib.FTP(server, timeout=10)
                ftp.login(ftp_user, ftp_password)

               
                with open(local_file_path, 'rb') as f:
                    ftp.storbinary(f'STOR {os.path.basename(remote_file_path)}', f)
                    print(f"Uploaded: {local_file_path} to {pc}")

                # Close the FTP connection
                ftp.quit()
                print(f"local watchdog sent to {pc} on network {network}")
            except Exception as e:
                print(f" --> FAILED!! {e}")
            else:
                break
            



if __name__ == "__main__":

    main()

