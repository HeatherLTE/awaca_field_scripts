#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 11:28:45 2024

@author: corden
"""

#plot defaults for the mrr variables

plot_defaults = {
    
    'Ze': {
        'cmap': 'Spectral_r',
        'zrange': [-60, 30],
        'long_name': r'Equivalent Reflectivity $Z_e$ [dBZ]'
        },
    
    'Z': {
        'cmap': 'Spectral_r',
        'zrange': [-60, 30],
        'long_name': r'Reflectivity $Z$ [dBZ]'
        },
    
    'VEL': {
        'cmap': 'bwr',
        'zrange': [-8, 5],
        'long_name': r'Mean Radial Velocity [m s$^{-1}$]'
        },
    
    
    'WIDTH': {
        'cmap': 'Spectral_r',
        'zrange': [0, 2.5],
        'long_name': r'Doppler Spectrum Width [m s$^{-1}$]'
        }, 
    
    'SNR': {
        'cmap': 'Spectral_r',
        'zrange': [-10, 50],
        'long_name': r'SNR [dB]'
        },
    
    'RR': {
        'cmap': 'viridis',
        'zrange': [0, 40],
        'long_name': r'Rain Rate [mm hr$^{-1}$]'
        },
        
    }
