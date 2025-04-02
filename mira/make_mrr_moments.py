#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 09:57:44 2024

@author: corden
"""

# a script for extracting only moments from the mrr znc files

import os
import datetime as dt
import pandas as pd
import xarray as xr #will need to use a python env with xarray



####### VARIABLES TO CHANGE #########

operational = True #only try to plot the last three days from today
start_date = dt.date(2024, 12, 5) #  not used if operational=true
end_date = dt.date(2024, 12, 11) # not used if operational=true

fpath_data = '/mom/mrr/'
moments_outpath = '/mom/mrr_moments/'

#laptop testing
fpath_data = '/data/awaca_onsite_data/raid/d17/mrr/data/'
moments_outpath = '/home/corden/Documents/miniprojects_tests/mira_moment_files/mrr/'

overwrite = False #whether to overwrite plots that have already been made


########################################

# operational mode only considers files measured in the last three days starting with yesterday
if operational:
    end_date = (dt.datetime.utcnow() - dt.timedelta(days=1)).date() #don't try to do the files from today as they might still be being written
    start_date = end_date - dt.timedelta(days = 3)

days_to_search = pd.date_range(start_date, end_date, freq = "D")

def extract_moments(inpath_file, outpath_folder, overwrite):
    
    filename = os.path.basename(inpath_file)
    new_filename = filename.split('.')[0] + '_moments' +'.nc'
    outpath_file = os.path.join(outpath_folder, new_filename)
   
    if not overwrite:
        if os.path.exists(outpath_file):
            print(f'moments file exists for {filename}, skipping')
            return

    ds = xr.open_dataset(inpath_file)
        
    ds.drop_dims(['n_spectra', 'spectrum_n_samples']).to_netcdf(outpath_file)
    ds.close()
    return None
            

print('********************* Producing MRR Moment Files ************************************')


for plotday in days_to_search:
    inpath_folder = os.path.join(fpath_data, plotday.strftime("%Y%m/%Y%m%d")) #in metek format
    outpath_folder = os.path.join(moments_outpath, plotday.strftime("%Y"), plotday.strftime("%m"), plotday.strftime("%d")) #in format for simple sync to epfl
    
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
            
        
     
            


            

        


