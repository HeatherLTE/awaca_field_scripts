#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 00:49:05 2024 (don't worry, it is 0949 in DDU)

# config file for the data transfer 
# between the AWACA raid
# and the epfl servers

# in the form of a python dictionary to allow for many subsections

@author: corden
"""

config = {
    
    'd17':{
        'mira':{
            'path_quicklooks': '/home/data/awaca_scriptsnlogs/quicklook_plots/mira/',
            'path_logs': '/home/data/awaca_scriptsnlogs/logs/',
            'path_data': '/mom/',
            'port_ssh_epfl': 9017
            },
        'mrr':{
        'path_quicklooks': '/home/data/awaca_scriptsnlogs/quicklook_plots/mrr/',
        'path_data': '/mom/mrr/',
        'path_logs': '/home/data/awaca_scriptsnlogs/logs/'
        
            }
        },
    
    'd47':{
        'mira':{
            'path_quicklooks': '/home/data/awaca_scriptsnlogs/quicklook_plots/mira/',
            'path_logs': '/home/data/awaca_scriptsnlogs/logs/',
            'path_data': '/mom/',
            'port_ssh_epfl': 9047
            },
        'mrr':{
        'path_quicklooks': '/home/data/awaca_scriptsnlogs/quicklook_plots/mrr/',
        'path_data': '/mom/mrr/',
        'path_logs': '/home/data/awaca_scriptsnlogs/logs/'
            }
        },
    
    'd85':{
        'mira':{
            'path_quicklooks': '/home/data/awaca_scriptsnlogs/quicklook_plots/mira/',
            'path_logs': '/home/data/awaca_scriptsnlogs/logs/',
            'path_data': '/mom/',
            'port_ssh_epfl': 9085
            },
        'mrr':{
        'path_quicklooks': '/home/data/awaca_scriptsnlogs/quicklook_plots/mrr/',
        'path_data': '/mom/mrr/',
        'path_logs': '/home/data/awaca_scriptsnlogs/logs/'
            }
        },
    
    'dmc':{
        'mira':{
            },
        'mrr':{
            }
        },
    
    'all':{
        'mira_user': 'data',
        },
        
    'epfl':{
        'user':'lteuser',
        'server':'ltesrv5',
        'archive':'/awaca/raid'
        #'archive':'/home/corden/ltedatatrial/awaca/raid'
        }
    
    
    }
