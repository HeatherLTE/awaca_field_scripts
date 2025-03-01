#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 09:37:22 2024

@author: corden
"""


import os
import re
import itertools
import datetime as dt
import pandas as pd
import numpy as np

def find_mrr_zenith_files(start_datetime, end_datetime, 
                             search_fpath = '/home/corden/Documents/miniprojects_tests/mrr_guyancourt/data/', 
                             date_structure_metek = False,
                             full_path = True,
                             pattern = "", exclude = ["PPI", "RHI"]):
    """
    find all the mrr zenith files between two times
    For plotting on a time-height plot

    Parameters
    ----------
    start_datetime : datetime.datetime
        
    end_datetime : datetime.datetime
    
    full_path : boolean optional
        whether to return the full file path or not
        The default is True    
    search_fpath : string, optional
        where to look for the date-organised moments files
        The default is '/home/corden/Documents/miniprojects_tests/mrr_guyancourt/data/'.
    date_structure_metek : boolean, optional
        Whether to use the date structure as used by metek on the mrr (%Y%m/%Y%m%d/).
        Or, if False, use the structure (%Y/%m/%d/).
        The default is False.
    pattern : string, optional
        patterns that should be included in desired file names
        The default is "".
    exclude : list of strings, optional
        Strings in filenames that should be excluded. The default is ["PPI", "RHI"] (ie exclude scans).

    Returns
    -------
    files_subset : list of strings
        list of full filepaths of desired files.

    """
    
    days_to_search = pd.date_range(start_datetime.date(), end_datetime, freq = "D")
    
    if date_structure_metek:
        paths_to_search = [os.path.join(search_fpath, day.strftime("%Y%m/%Y%m%d")) for day in days_to_search]
    else:
        paths_to_search = [os.path.join(search_fpath, day.strftime("%Y/%m/%d")) for day in days_to_search]
        
    
    #first list all files, keeping the full path
    #there are just too many iterations for a list comprehension, use a for loop for now
    all_files = []
    for fpath in paths_to_search:
        files_one_day = os.listdir(fpath)
        full_paths_one_day = [os.path.join(fpath, i) for i in files_one_day]
        all_files.extend(full_paths_one_day)
        
    if len(all_files) == 0:
        print(f"no files found for {fpath}, returning None")
        return None
    
    #then filter for file type and any required patterns
    nc_files = [i for i in all_files if ('.nc' in i)] #only want .nc netcdf files, not the log files
    correct_files = [i for i in nc_files if (pattern in i) and not any(e in i for e in exclude)]
    
    if len(correct_files) == 0:
        print(f"no files of correct type found for {fpath}, returning None")
        return None
    
    #then filter for date
    date_strings = [re.search('\d{8}_\d{6}', i).group() for i in correct_files]
    dates = [dt.datetime.strptime(i, "%Y%m%d_%H%M%S") for i in date_strings]


    mask = np.array([start_datetime <= i <= end_datetime for i in dates])
    files_subset = np.array(correct_files)[mask]
    
    if len(files_subset) == 0:
        print(f"no files meeting date requirement found for {fpath}, returning None")
        return None
    
    if not full_path:
        #convert to only filenames
        files_subset = [i.split('/')[-1] for i in files_subset]
    
    return files_subset

def zenith_full_day_files(day_string_or_datetime, extend = False, 
                          search_fpath = '/ltedata/Eriswil_2024/StXPOL/Raw_data/moments/', 
                          date_structure_metek = False, 
                          pattern = "", exclude = ["PPI", "RHI"]):
    """
    wrapper function to find files for plotting a full day of zenith files

    Parameters
    ----------
    day_string_or_datetime : string in format YYYYMMDD or datetime.datetime
        The day to find all files for.
    extend : boolean, optional
        Whether to look for files from the previous day which might overlap onto the desired day. The default is True.
    search_fpath : string, optional
        where to look for the date-organised moments files
        The default is '/ltedata/Eriswil_2024/StXPOL/Raw_data/moments/'.
    date_structure_metek : boolean, optional
        Whether to use the date structure as used by metek on the mrr (%Y%m/%Y%m%d/).
        Or, if False, use the structure (%Y/%m/%d/).
        The default is False.
    pattern : string, optional
        patterns that should be included in desired file names
        The default is "".
    exclude : list of strings, optional
        Strings in filenames that should be excluded. The default is ["PPI", "RHI"] (ie exclude scans).

    Returns
    -------
    None.

    """
    
    if isinstance(day_string_or_datetime, str):
        today = dt.datetime.strptime(day_string_or_datetime, '%Y%m%d')
        
    if isinstance(day_string_or_datetime, dt.datetime):
        today_start = day_string_or_datetime.date()
        today = dt.datetime(today_start.year, today_start.month, today_start.day)
        
    if isinstance(day_string_or_datetime, dt.date):
        today = dt.datetime(day_string_or_datetime.year, day_string_or_datetime.month, day_string_or_datetime.day)
        
    end_datetime = today + dt.timedelta(hours = 23, minutes = 59, seconds = 59)
        
    if extend:
        #look for files starting after 23:55 on the previous day which might overlap onto the current day
        yesterday = today - dt.timedelta(minutes = 5)
        start_datetime = dt.datetime(yesterday.year, yesterday.month, yesterday.day, yesterday.hour, yesterday.minute)
    else:
        start_datetime = today
    
    files = find_mrr_zenith_files(start_datetime, end_datetime, search_fpath = search_fpath, date_structure_metek=date_structure_metek, pattern = pattern, exclude = exclude)
    
    return files
        


    
        

