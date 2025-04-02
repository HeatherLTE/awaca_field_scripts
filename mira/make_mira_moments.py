#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 09:57:44 2024

@author: corden
"""

# a script for extracting only moments from the mira .znc files

import os
import datetime as dt
import pandas as pd
import xarray as xr #will need to use a python env with xarray



####### VARIABLES TO CHANGE #########

operational = True #only try to plot the last three days from today
start_date = dt.date(2024, 12, 10) #  not used if operational=true
end_date = dt.date(2024, 12, 11) # not used if operational=true

fpath_data = '/mom/'
moments_outpath = '/mom/mira_moments/'

#laptop testing
#fpath_data = '/data/awaca_onsite_data/raid/d17/mira/data/'
#moments_outpath = '/home/corden/Documents/miniprojects_tests/mira_moment_files/'

overwrite = False #whether to overwrite plots that have already been made


########################################

# operational mode only considers files measured in the last three days starting with yesterday
if operational:
    end_date = (dt.datetime.utcnow() - dt.timedelta(days=1)).date()
    start_date = end_date - dt.timedelta(days = 3)

days_to_search = pd.date_range(start_date, end_date, freq = "D")

def extract_moments(inpath_file, outpath_folder, overwrite):
    
    filename = os.path.basename(inpath_file)
    new_filename = filename.split('.')[0] + '_moments' +'.znc'
    outpath_file = os.path.join(outpath_folder, new_filename)
   
    if not overwrite:
        if os.path.exists(outpath_file):
            print(f'moments file exists for {filename}, skipping')
            return

    ds = xr.open_dataset(inpath_file)
        
    ds.drop_dims('doppler').to_netcdf(outpath_file)
    ds.close()
    return None
            

print('********************* Producing MIRA Moment Files ************************************')


for plotday in days_to_search:
    inpath_folder = os.path.join(fpath_data, plotday.strftime("%Y"), plotday.strftime("%m"), plotday.strftime("%d"))
    outpath_folder = os.path.join(moments_outpath, plotday.strftime("%Y"), plotday.strftime("%m"), plotday.strftime("%d"))
    
    #make subdirectories if they don't exist
    if not os.path.exists(outpath_folder):
        os.makedirs(outpath_folder)
    
        
    try:   
        for file in os.listdir(inpath_folder):
            print(file)
            inpath_file = os.path.join(inpath_folder, file)
            try:
                extract_moments(inpath_file, outpath_folder, overwrite)
            except Exception as e:
                print(e)
                print('continuing...')
    except Exception as e:
        print(e)
        print('continuing...') 
            
        
     
            


            

        


