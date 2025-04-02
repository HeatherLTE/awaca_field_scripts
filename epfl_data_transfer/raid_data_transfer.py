#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 00:18:48 2024

# a script to transfer things (= quicklooks, log files, data)
# from the computers in the OPUs of the AWACA Raid
# to the LTE servers
# using rsync
# to be called via crontab with arguments

# configurable filepaths are saved in the python file config_raid_epfl_transfer.py
# in the form of a python dictionary (to allow for many subsections)

@author: corden
"""
import argparse
import datetime
import os
import subprocess
from config_raid_epfl_transfer import config

def main():
    print(f"--------------{datetime.datetime.utcnow()}---------------")
    
    ## parse arguments from the terminal
    
    parser = argparse.ArgumentParser(description="Transfer things from the AWACA Raid to EPFL")
    parser.add_argument("site", help="site of the OPU to copy data from: d17, d47, d85, dmc")
    parser.add_argument("instrument", help="mira or mrr, lowercase")
    parser.add_argument("what", help="What should be transferred: quicklooks, logs or data")
    #read the number of days to sync - this reduces file comparisons and allows for correct subfolder handling. Set to a large number to sync the whole archive
    parser.add_argument("-n","--no_of_days_to_sync",  type = int, help = 'the number of days to sync, optional, default 10')
    parser.add_argument("-d", "--start_day",  help = 'as YYYYMMDD, the start day for the data to be synced, optional, default today')
    
    args = parser.parse_args()

    site = args.site
    instrument = args.instrument
    what = args.what
    ndays = args.no_of_days_to_sync if args.no_of_days_to_sync else 10
    start_day = datetime.datetime.strptime(args.start_day, '%Y%m%d') if args.start_day else datetime.datetime.utcnow()
    
    
    print(f'Transferring {what} for the {site} {instrument} for the {ndays} days ending on {start_day.strftime("%Y.%m.%d")}')
    
    #site = 'D17'
    #instrument = 'MIRA'
    #what = 'quicklooks'
    #ndays = 10
    
    ## read the correct paths from the config file
    # 'archive' gives the parent path up to the point of date subfolders
    raid_archive = config[site][instrument]['path_' + what]
    epfl_archive = os.path.join(config['epfl']['archive'], site, instrument, what)
    print(epfl_archive)
    if not os.path.exists(epfl_archive):
        try:
            print(f'The correct local folder does not exist, creating folder {epfl_archive}')
            os.makedirs(epfl_archive) 
        except Exception as e:
            print(f'Failed to create local folder: {e}')
    
    #make a list of days to sync
    
    days_to_sync = [start_day - datetime.timedelta(days = i) for i in range(ndays)] 
    
    ## loop through days to sync
    for day in days_to_sync:
        raid_folder, epfl_folder = add_date_subfolders(raid_archive, epfl_archive, day, instrument, what)
        if not os.path.exists(epfl_folder):
            try:
                print(f'Creating new subfolder {epfl_folder}')
                os.makedirs(epfl_folder)
            except Exception as e:
                print(f'Failed to create new local subfolder: {e}')
                
        try:
            sync_epfl_raid(raid_folder, epfl_folder, site)
        except:
            print(f'an error occurred whilst syncing {day.strftime("%Y/%m/%d")}, continuing to the next day')
            continue
        
    # tidy up by deleting newly created subfolders if nothing was copied into them (makes it easier to see days without data)
    delete_empty_folders(epfl_archive)
   
        
    
def add_date_subfolders(raid_archive, epfl_archive, day, instrument, what):
    """
    Add date subfolders to the folders to sync between the raid and epfl

    Parameters
    ----------
    raid_archive : string, path
        The path of the thing to sync on the raid, up to the point of date subfolders.
    epfl_archive : string, path
        The destination path at epfl, up to the point of date subfolders.
    day : datetime.datetime
        the day to sync, for creating the correct subfolders.
    instrument : string
        MIRA or MRR, different subfolder structure for MRR.
    what : string
        data, quicklooks or logs.

    Returns
    -------
    raid_folder : string, path
        remote folder with correct date subfolders.
    epfl_folder : string, path
        local folder with correct date subfolders.

    """
    
    ## epfl folder
    if what in ['data', 'quicklooks']:
        # all data on epfl server should be in YYYY/MM/DD subfolders
        epfl_folder = os.path.join(epfl_archive, day.strftime("%Y"), day.strftime("%m"), day.strftime("%d"))
    else:
        #logs are not in subfolders
        epfl_folder = epfl_archive
    
    ## raid folder
    if (instrument == 'mrr') and (what == 'data'):
        #MRR annoyingly has different folder structure
        raid_folder = os.path.join(raid_archive, day.strftime("%Y%m"), day.strftime("%Y%m%d"))
        
    elif (what in ['data', 'quicklooks']):
        raid_folder = os.path.join(raid_archive, day.strftime("%Y"), day.strftime("%m"), day.strftime("%d"))
    else:
        # log files are not in subfolders
        raid_folder = raid_archive
        
    return raid_folder, epfl_folder



def sync_epfl_raid(raid_folder, epfl_folder, site):
    
    port_mira = config[site]['mira']['port_ssh_epfl']
    user_mira = config['all']['mira_user']
    
    #make sure each folder has a slash at the end, so that we copy the content of the folder rather than the folder itself
    if not raid_folder.endswith('/'):
        raid_folder += '/'
        
    if not epfl_folder.endswith('/'):
        epfl_folder += '/'
    
    
    process = subprocess.Popen(
        [
            'rsync',
            '-ave',
            f'ssh -p {port_mira}', #change the port, read from config file. Note that MRR files are accessed from the MIRA of the same OPU!
            '--stats',
            f'{user_mira}@localhost:{raid_folder}', 
            epfl_folder
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    """
    #local trial
    process = subprocess.Popen(
        [
            'rsync',
            '-av',
            '--stats',
            raid_folder, 
            epfl_folder
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    """
    
    stdout, stderr = process.communicate()
    if stderr:
        print(f'rsync error: {stderr}')
    else:
        print(stdout)
    
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
