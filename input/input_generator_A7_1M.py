# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 14:23:33 2018

@author: NguyenTran
"""

import yaml;
import numpy as np;
from math import log;
import copy;

#import inflect;
#p = inflect.engine();

def kFormatter(num):
    return str(num) if num <=999 else str(round(num/1000)) +'k';


stream = open('input_base_A7_mu_0p001983_v2.yml', 'r');
data = yaml.load(stream);
stream.close();

 # COMMENT IT LATER
# data['ending_date'] = '2022/1/1';

location_info =  [[0, 0, 0]];
number_of_locations = len(location_info);
data['location_db']['location_info']= location_info;

#population size 
popsize = 1000000
data['location_db']['population_size_by_location'] = [popsize];       


tcs = {
       # 0.25: {
       #     'tc_str': '0p25',
       #     'pfprs': {
       #         0.13: 'PFPR10p0',
       #         0.049: 'PFPR01p0',
       #         0.044: 'PFPR00p1'
       #         }           
       #     },
       0.5: {
           'tc_str': '0p50',
           'pfprs': {
               0.15: 'PFPR10p0',
               0.057: 'PFPR01p0',
               0.051: 'PFPR00p1'
               }           
           },
       # 0.75: {
       #     'tc_str': '0p75',
       #     'pfprs': {
       #         0.16: 'PFPR10p0',
       #         0.066: 'PFPR01p0',
       #         0.0585: 'PFPR00p1'
       #         }           
       #     },
       }

tact = {
        0: 'DP',
        4: 'ALAQ',
        5: 'AMP'
        }
#%%
tact_adoption = {
    0.5: {
        'ta_str': '0p5',
        },
    1.5: {
        'ta_str': '1p5',
        },
    2.5: {
        'ta_str': '2p5',
        },
    3.5: {
        'ta_str': '3p5',
        },
    4.5: {
        'ta_str': '4p5',
        },
    }
    

#%%
for tc, tc_details in tcs.items():
    tc_str = tc_details['tc_str'];
    pfprs = tc_details['pfprs'];
    for beta,pfpr in pfprs.items():
        for tact_id, tact_str in tact.items():                
            for ta, ta_details in tact_adoption.items():
                ta_str = ta_details['ta_str']
                peak_after =  round((0.8-0.674854)*365.25*100/ta)
                
                print(beta, tc_str, tact_id, peak_after)
                new_data = copy.deepcopy(data)
                new_data['location_db']['beta_by_location'] = np.full(number_of_locations, beta).tolist()
                
                new_data['location_db']['p_treatment_for_less_than_5_by_location'] = np.full(number_of_locations, tc).tolist()
                new_data['location_db']['p_treatment_for_more_than_5_by_location'] = np.full(number_of_locations, tc).tolist()
                
                for index,event in enumerate(data['events']):                    
                    if event['name'] == 'modify_nested_mft_strategy':
                        new_data['events'][index]['info'][0]['strategy_id'] = tact_id
                
                new_data['strategy_db'][7]['peak_after'] = peak_after
                
                output_filename = 'A7_1M/TACT_%s_TC_%s_TACT_%s_tact_adoption_%s.yml'%( pfpr,tc_str, tact_str,ta_str);
                output_stream = open(output_filename, 'w');
                yaml.dump(new_data, output_stream); 
                output_stream.close();

#%%
for ta, ta_details in tact_adoption.items():
    ta_str = ta_details['ta_str']
    peak_after =  round((0.8-0.674854)*365.25*100/ta)
    print(peak_after)