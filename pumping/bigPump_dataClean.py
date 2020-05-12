# -*- coding: utf-8 -*-
"""
Created on Mon May 11 10:26:12 2020

@author: iordach1
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

input_file_IWIP = "Pumpage_Data_GRL_all.csv"
IWIP_df = pd.read_csv(input_file_IWIP, dtype = {'isws_facility_id': str, 'p_num': str})

for row in IWIP_df.iterrows():
    if pd.isnull(row[1][5]) or pd.isnull(row[1][6]):
        IWIP_df.drop(row[0], inplace = True)
        

IWIP_df.reset_index(inplace = True, drop = True)
print("Removed wells without location data")

for row in IWIP_df.iterrows():
    if pd.isnull(row[1][7:]).all():
        IWIP_df.drop(row[0], inplace = True)
        
IWIP_df.reset_index(inplace = True, drop = True)
print("Removed wells without pumpage data")

for row in IWIP_df.iterrows():
    if pd.isnull(row[1][4]) or row[1][4] < 0:
        IWIP_df.drop(row[0], inplace = True)
        
IWIP_df.reset_index(inplace = True, drop = True)
print("Removed wells without depth")

for row in IWIP_df.iterrows():
    if row[1][1][3] == '7':
        IWIP_df.drop(row[0], inplace = True)
        
IWIP_df.reset_index(inplace = True, drop = True)
print("Removed ag irrigation wells")


facility_pump = pd.pivot_table(
            IWIP_df,
            index = ['isws_facility_id', 'owner'],
            aggfunc = 'sum'
        ).reset_index()

facility_pump = facility_pump.iloc[:, :-4]

static_df = facility_pump.copy(deep = 'True')

max_pump = []

for row in static_df.itertuples():
    max_pump.append(max(row[3:]))
    
static_df['max_pump'] = max_pump

static_df = static_df.sort_values('max_pump', ascending = False).head(10)

static_df = static_df.drop(129).replace(0, np.nan)

trans_df = facility_pump.transpose()

facility_pump2 = trans_df.iloc[2:].astype('float').replace(0, np.nan).interpolate(limit_area = 'inside')
print("Interpolated between data gaps")

for column in facility_pump2:
    for i in range(2012,2020):
        if not pd.isna(facility_pump2[column][str(i)]):
            facility_pump2[column][str(i):] = facility_pump2[column][str(i):].fillna(method='ffill')
print("Forward fill last 7 years of data")
        
facility_pump.iloc[:,2:] = facility_pump2.transpose()

max_pump = []

for row in facility_pump.itertuples():
    max_pump.append(max(row[3:]))
    
facility_pump['max_pump'] = max_pump

facility_pump = facility_pump.drop(129)

facility_pump = facility_pump.sort_values('max_pump', ascending = False).head(10)

#%%plots


for row in facility_pump.head().iterrows():
    plt.figure(figsize=(17,11))
    plt.plot([x for x in range(1981, 2020)], row[1][2:-1], '--', label = 'Interpreted', linewidth =4)
    plt.plot([x for x in range(1981, 2020)], static_df[static_df['isws_facility_id'] == row[1][0]].iloc[:,2:-1].values.tolist()[0], label = 'Original', linewidth = 5)
    plt.title("IWIP Facility: {0} [{1}]".format(row[1][0], row[1][1]), fontsize = 24)
    plt.xlim(1981, 2018)
    plt.subplot().set_ylabel('Annual Pumpage [GALLONS]', fontsize = 20)#ylabel
    plt.subplot().tick_params(axis='both', which='major', labelsize=16)
    plt.subplot().tick_params(axis='both', which='minor', labelsize=12)
    plt.subplot().yaxis.get_offset_text().set_size(16)
    plt.legend()
    plt.savefig("{0}.jpg".format(row[1][0]))
    plt.clf()