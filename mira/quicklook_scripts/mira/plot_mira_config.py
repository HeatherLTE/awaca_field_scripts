#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 11:28:45 2024

@author: corden
"""

# a script to give default colourbars params etc for the variables provided by mira
#using a dictionary for now but maybe this is not the best option - could use json or classes
#the keys are the variable keys as in the stxpol netcdf 
#maybe define global defaults for eg. reflectivity

plot_defaults = {
    
    'Zg': {
        'cmap': 'Spectral_r',
        'zrange': [-60, 30],
        'long_name': r'Reflectivity of all Targets [dBZ]'
        },
    
    'VELg': {
        'cmap': 'bwr',
        'zrange': [-8, 5],
        'long_name': r'Mean Radial Velocity [m s$^{-1}$]'
        },
    
    
    'RMSg': {
        'cmap': 'Spectral_r',
        'zrange': [0, 2.5],
        'long_name': r'Doppler Spectrum Width [m s$^{-1}$]'
        }, 
    
    
    'LDRg': {
        'cmap': 'Spectral_r',
        'zrange': [-30,0],
        'long_name': r'Linear Depolarisation Ratio $LDR$ [dB]'
        },
    
    'RHO': {
        'cmap': 'Spectral_r',
        'zrange': [0,1],
        'long_name': r'V-H Correlation $\rho_{HV}$'
        },
    
    'SNRg': {
        'cmap': 'Spectral_r',
        'zrange': [-10, 50],
        'long_name': r'SNR [dB]'
        },
    
   
    
    'DPS': {
        'cmap': 'Spectral_r',
        'zrange': [-360, 360],
        'long_name': r'Differential Phase $\Phi_{DP}$ [$^\{circ}$]'
        },
        
    }
