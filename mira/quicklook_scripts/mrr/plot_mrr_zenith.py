#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 08:09:49 2024

@author: corden
"""

#just for mrr



def plot_mrr_zenith(dsorfilepaths,
                       variable = 'Ze',
                       figsize = [10,4],
                       addcbar = True,
                       ylim = [0,6000],
                       zrange = 'auto',
                       long_name = 'auto',
                       heightaskm = False,
                       fix2day = False,
                       cmap = 'auto',
                       filtersnr = True,
                       snrvariable = 'SNR',
                       snrthreshold = -20,
                       plotgrid = False,
                       dateformat = '%H:%M',
                       saveplot = False,
                       saveasplot = 'auto',
                       outpath = '',
                       dpi = 300,
                       ):
    """
    Plot a time-height plot of mrr-pro moments data (from the .nc files from the radar). Produces a plot of one variable.
    
   
    Parameters
    ----------
    dsorfilepaths : xarray dataset or full filepath or list of full filepaths (string)
        Data to plot. Note that if multiple filepaths are passed, they are plotted individually on the same axes.
    variable : string, optional
        Which variable in the netcdf to plot. The default is 'DBZHC'.
    figsize : tuple, optional
        The default is [10,4].
    addcbar : boolean, optional
        Whether to plot colour bar. The default is True.
    ylim : tuple, optional
        Y limits in m above the radar. The default is [0,6000].
    zrange : tuple, optional
        Limits for the colourbar of the variable to be plotted. The default is 'auto'. This takes sensible ranges from plot_mrr_config.py
    long_name : string, optional
        Variable title for the colourbar. The default is 'auto'. This takes the value in plot_mrr_config.py
    heightaskm : boolean, optional
        Whether to plot the height axis in km. The default is False.
    fix2day : boolean, optional
        Fix the time axis to a whole day. The default is False.
    cmap : string, optional
        Which colour map to use. The default is 'auto'. This takes the value in plot_mrr_config.py
    filtersnr : boolean, optional
        Whether to filter values to be plotted based on the SNR. The default is True.
    snrvariable : string, optional
        Variable in the netcdf to use for the snr filtering. The default is 'SNRHC'.
    snrthreshold : float, optional
        Threshold in db for the snr. Values of the 'variable' will be plotted where the snr is above this value. The default is -18.6.
    plotgrid : boolean, optional
        Whether to plot a height-time grid. The default is False.
    dateformat : string, optional
        Date format string for the time axis. The default is '%H:%M'.
    saveplot : boolean, optional
        Whether to save the plot. The default is False.
    saveasplot : string, optional
        Filename to save the plot. The default is 'auto'. This creates a filename using the first and last times in the file.
    outpath : string, optional
        path of the folder to save the plot in. The default is ''.
    dpi :  optional
         The default is 300.

    Returns
    -------
    fig : matplotlib figure
    ax : matplotlib axes
    

    """
    
    #imports
    import os
    import numpy as np
    import pandas as pd
    import xarray as xr
    import datetime as dt
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import matplotlib.colors as mcolors
    from matplotlib.ticker import AutoMinorLocator, MultipleLocator
    
    #plot defaults and helper functions
    from mrr.plot_mrr_config import plot_defaults
    
    #convert to list to be able to use for loop
    if isinstance(dsorfilepaths, str) or isinstance(dsorfilepaths, xr.Dataset):
        dsorfilepaths = [dsorfilepaths]
        
    #initialise figure
    fig,ax = plt.subplots(1, figsize=figsize)
    
    #lists to store the first and last times in the files to plot
    first_times = []
    last_times = []

    for dsorfile in dsorfilepaths:
        #print(dsorfile)
        try:
        
            #open dataset if not already open
            if isinstance(dsorfile, str):
                ds = xr.open_dataset(dsorfile)  
            elif isinstance(dsorfile, xr.Dataset):
                 ds = dsorfile
            else:
                print("The data to plot should be passed as a filepath or an xarray dataset")
            
            
            
            x = ds.time.values
            y = ds.range.values
            
            try:
                z = ds[variable].T #use z as a general name for the values to be plotted
                #print(np.nanmax(z))
                #print(np.count_nonzero(~np.isnan(z)))
            except KeyError:
                print(f'variable {variable} not found, continuing to next file or dataset')
                continue
            
            
                
            #save the first and last times to use in an auto filename
            first_times.append(x[0])
            last_times.append(x[-1])
            
            # try reading defaults from config dictionary imported from plot_stxpol_defaults
            if zrange == 'auto':
                zrange = plot_defaults[variable]['zrange']
            else:
                zrange = zrange
                
            if cmap == 'auto':
                cmap = plot_defaults[variable]['cmap']
            else:
                cmap = cmap
            
            if long_name == 'auto':
                long_name = plot_defaults[variable]['long_name']
            else:
                long_name = long_name
                
            
            #filter for signal to noise ratio  
            if filtersnr:
                    
                snr = ds[snrvariable].T
                #print(np.max(snr).item(), np.min(snr).item())
                z = z.where(snr > snrthreshold)
                
            ds.close()
                
            # use a zero-centred colormap for velocity variables
            if 'VEL' in variable:
                z = -1*z #mrr stores velocity with positive towards radar
                mynorm = mcolors.TwoSlopeNorm(vmin = zrange[0], vcenter = 0, vmax=zrange[1])
            else:
                mynorm = mcolors.Normalize(vmin = zrange[0], vmax=zrange[1])
            
            #do the plotting
            im0=ax.pcolormesh(x, y, z , cmap=cmap, norm = mynorm)
        except:
            print(f'error with file {dsorfile}, continuing...')
            continue
            
        

    #add the colorbar
    if addcbar:
        cbar = fig.colorbar(im0, ax=ax, label=long_name, pad = 0.02)
        cbar.ax.set_yscale('linear') #change to equal tick spacing rather than equal colour gradient

    #format x axis
    
    if fix2day:
        t0 = min(first_times).astype('datetime64[s]').astype(dt.datetime) #have to convert to s first as otherwise return an int
        t1 = max(last_times).astype('datetime64[s]').astype(dt.datetime)
        xrange_new = ['','']
        xrange_new[0] = pd.to_datetime(t0 + dt.timedelta(minutes = 10)).floor('1D') # have to use pandas in order to have the floor functionality
        xrange_new[1] = pd.to_datetime(t1 - dt.timedelta(minutes = 10)).ceil('1D')
       
        ax.set_xlim(xrange_new)
        
        #add the day as title
        ax.set_title(f'MRR Zenith {xrange_new[0].strftime("%d/%m/%Y")}', loc = 'right', color = 'grey', fontsize = '10')
        
        
    ax.set_xlabel('Time [UTC]')
    myFmt = mdates.DateFormatter(dateformat)
    hours = mdates.HourLocator()
    ax.xaxis.set_major_formatter(myFmt)
    ax.xaxis.set_minor_locator(hours)
    
    #format y axis
    ax.set_ylabel('Height Above Radar [m]')
    ax.set_ylim(ylim)
    ax.yaxis.set_minor_locator(AutoMinorLocator(4))
    
    if heightaskm:
        y_vals = ax.get_yticks()
        ax.set_yticks(y_vals)
        ax.set_yticklabels(['{:,.2f}'.format(x /1000) for x in y_vals])
        ax.set_ylabel('Height Above Radar [km]')
    

    if plotgrid:
        ax.grid()
        
            
    #machinery to save plot
    if saveplot:
        if saveasplot == 'auto':
            t0 = min(first_times).astype('datetime64[s]').astype(dt.datetime) #have to convert to s first as otherwise return an int
            t1 = max(last_times).astype('datetime64[s]').astype(dt.datetime)
            filename = f'{t0.strftime("%Y%m%d%H%M%S")}_{t1.strftime("%Y%m%d%H%M%S")}_mrr_zenith_{variable}'
        else:
            filename = saveasplot
            
        if not filename.endswith('.png'):
            filename +='.png'
            
        fig.savefig(os.path.join(outpath, filename), dpi = dpi, bbox_inches = 'tight')
        
        # check the file really saved where you thought
        if os.path.exists(os.path.join(outpath, filename)):
            print('The plot was saved at')
            print(os.path.abspath(os.path.join(outpath, filename)))
        else:
            print("The plot was not saved correctly, file not found")
            
    return fig, ax






def plot_mrr_zenith_day(day_string_or_datetime,
                           fpath_moments,
                       variable = 'Zg',
                       figsize = [10,4],
                       addcbar = True,
                       ylim = [0,6000],
                       zrange = 'auto',
                       long_name = 'auto',
                       heightaskm = False,
                       cmap = 'auto',
                       filtersnr = True,
                       snrvariable = 'SNR',
                       snrthreshold = -18.6,
                       plotgrid = False,
                       dateformat = '%H:%M',
                       saveplot = False,
                       overwrite = True,
                       saveasplot = 'auto',
                       outpath = '',
                       dpi = 300,
                       returnfig = False
                       ):
    
    """
    a wrappper function for plot_mrr_zenith to simplify making zenith full day quicklooks, with added avoid overwrite functionality

    Parameters
    ----------
    Note that most parameters are passed to plot_mrr_zenith, only extra parameters are listed here
    
    day_string_or_datetime : string or datetime.datetime
        The day to plot. If a string is passed it should be in the format yyyymmdd
    overwrite : boolean, optional
        Whether to overwrite an existing plot for that day. The default is 'True'.
    returnfig : boolean, optional
        Whether to return the figure and axes objects. For operational quicklooks this should be set to False. The default is False.
    

    Returns
    -------
    fig : matplotlib figure
    ax : matplotlib axes
    If returnfig is False, returns None
    

    """
    import datetime as dt
    import matplotlib.pyplot as plt
    import os
    from mrr.find_mrr_zenith_files import zenith_full_day_files
    
    if isinstance(day_string_or_datetime, str):
        plot_day = dt.datetime.strptime(day_string_or_datetime, '%Y%m%d')
        
    if isinstance(day_string_or_datetime, dt.datetime):
        day_start = day_string_or_datetime.date()
        plot_day = dt.datetime(day_start.year, day_start.month, day_start.day)
        
    if isinstance(day_string_or_datetime, dt.date):
        plot_day = dt.datetime(day_string_or_datetime.year, day_string_or_datetime.month, day_string_or_datetime.day)
    
    #first check if plot already exists for that day
    if saveplot:
        
        if saveasplot == 'auto':
            filename = f'{plot_day.strftime("%Y%m%d")}_mrr_zenith_day_{variable}'
        else:
            filename = saveasplot
            
        if not filename.endswith('.png'):
            filename +='.png'
        
        if not overwrite:
            if os.path.exists(os.path.join(outpath, filename)):
                print(f'zenith full day plot exists for {plot_day.strftime("%Y%m%d")}, skipping')
                return
            
            
    
    #find the zenith files for that day
    files_one_day = zenith_full_day_files(day_string_or_datetime, extend = False, search_fpath = fpath_moments)
    
    if files_one_day is None:
        print(f'no zenith files found for {plot_day.strftime("%Y%m%d")}, returning None')
        return None
    
    #plot the zenith files for that day
    fig, ax = plot_mrr_zenith(files_one_day, variable = variable, figsize = figsize, addcbar = addcbar, ylim = ylim, zrange = zrange, 
                                 long_name = long_name, heightaskm = heightaskm, 
                                 fix2day = True, 
                                 cmap = cmap, 
                                 filtersnr = filtersnr, snrvariable = snrvariable, snrthreshold = snrthreshold, 
                                 plotgrid = plotgrid, dateformat = dateformat, 
                                 saveplot=False, #control saving in wrapper function
                                 outpath = outpath, dpi = dpi)
    
    #machinery to save plot
    if saveplot:
        #filename generated near the start of the function
            
        fig.savefig(os.path.join(outpath, filename), dpi = dpi, bbox_inches = 'tight')
        
        # check the file really saved where you thought
        if os.path.exists(os.path.join(outpath, filename)):
            print('The plot was saved at')
            print(os.path.abspath(os.path.join(outpath, filename)))
        else:
            print("The plot was not saved correctly, file not found")
    
    if returnfig:
        return fig, ax
    else:
        plt.clf()
        plt.close(fig)
        return None
    

            
        
        
        
        
        
    

    
    
    
    
    
    
