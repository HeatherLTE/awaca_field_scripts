#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 09:57:44 2024

@author: corden
"""

# a script for mira quicklooks
import os
import datetime as dt
import pandas as pd

from mira.plot_mira_znc_zenith import plot_mira_zenith_day

####### VARIABLES TO CHANGE #########
operational = True #only try to plot the last three days from today
start_date = dt.date(2024, 3, 13) # day to start making plots on - not used if operational=true
end_date = dt.date(2024, 3, 13) # day to stop making plots on -not used if operqtional=true


quicklook_variables = ['Zg', 'VELg', 'RMSg', 'LDRg', 'RHO'] #variables to plot
# options for variables are 

fpath_moments = '/mom/'
quicklooks_outpath = '/home/data/awaca_scriptsnlogs/quicklook_plots/mira/'
dpi = 100
overwrite = False #whether to overwrite plots that have already been made

zenith_ylim = [0, 9000]
snrthreshold = -100 #threshold of copolar SNR to filter plots
########################################

# operational mode only considers files measured in the last three days
if operational:
    end_date = dt.datetime.utcnow().date()
    start_date = end_date - dt.timedelta(days = 3)

days_to_search = pd.date_range(start_date, end_date, freq = "D")


            
########## Zenith quicklooks ##############
print('********************* Producing MIRA Zenith Full-Day Quicklooks ************************************')
# we want to keep reproducing-overwriting the file until the day is full, then not any more
# for all days before the current day, the number of files willl be constant so can use overwrite= False 
# for the current day, new files will appear so we want to keep making the plot

for plotday in days_to_search:
    
    full_outpath = os.path.join(quicklooks_outpath, plotday.strftime("%Y"), plotday.strftime("%m"), plotday.strftime("%d"))
    if not os.path.exists(full_outpath):
        os.makedirs(full_outpath)
    
    if plotday.date() == dt.datetime.utcnow().date():
        overwrite_zenith = True #for files made on the day of data recording, want to keep making the plot new
    elif plotday.date() == (dt.datetime.utcnow() - dt.timedelta(days=1)).date():
        #also remake the plot from yesterday to catch changes over midnight
        overwrite_zenith = True
    else:
        overwrite_zenith = overwrite
        
    for variable in quicklook_variables:
        try:
            plot_mira_zenith_day(plotday, fpath_moments = fpath_moments, 
                                   variable = variable, ylim = zenith_ylim, 
                                   snrthreshold = snrthreshold, saveplot = True, 
                                   overwrite = overwrite_zenith, 
                                   outpath = full_outpath, dpi = dpi)
        except Exception as e:
            print(e)
            print('continuing...')

            

        


