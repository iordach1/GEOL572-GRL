# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 14:48:57 2020

@author: iordach1
"""

import pandas as pd
import matplotlib.pyplot as plt

#%%read in data
input_file = "Pumpage_Data_GRL.csv"

df = pd.read_csv(input_file, dtype = {'isws_facility_id': str})

static_df = df.copy(deep = 'True')

#%%clean data
for row in df.iterrows():
    if pd.isnull(row[1][5]) or pd.isnull(row[1][6]):
        df.drop(row[0], inplace = True)
        

df.reset_index(inplace = True, drop = True)
print("Removed wells without location data")

for row in df.iterrows():
    if pd.isnull(row[1][7:]).all():
        df.drop(row[0], inplace = True)
        
df.reset_index(inplace = True, drop = True)
print("Removed wells without pumpage data")

trans_df = df.transpose()

df2 = trans_df.iloc[7:].astype('float').interpolate(limit_area = 'inside')
print("Interpolated between data gaps")

for column in df2:
    for i in range(2012,2019):
        if not pd.isna(df2[column][str(i)]):
            df2[column][str(i):] = df2[column][str(i):].fillna(method='ffill')
print("Forward fill last 6 years of data")
        
df.iloc[:,7:] = df2.transpose()

df.to_csv("Pumpage_Data_GRL_mod.csv")

#%%plots


for row in df.sample(5).iterrows():
    #print(row[1])
    x=static_df[static_df['p_num'] == row[1][0]].iloc[:,7:].values.tolist()[0]
    print(x)
    plt.figure(figsize=(17,11))
    plt.plot([x for x in range(1981, 2019)], row[1][7:], '--', label = 'mod', linewidth =3)
    plt.plot([x for x in range(1981, 2019)], static_df[static_df['p_num'] == row[1][0]].iloc[:,7:].values.tolist()[0], label = 'orig', linewidth = 3)
    plt.title("Well p_num: {0}".format(row[1][0]))
    plt.xlim(1981, 2018)
    plt.legend()
    plt.savefig("{0}.jpg".format(row[1][0]))
    plt.clf()
    

    