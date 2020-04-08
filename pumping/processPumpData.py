# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 14:48:57 2020

@author: iordach1
"""

import pandas as pd

input_file = "Pumpage_Data_GRL.csv"

df = pd.read_csv(input_file, dtype = {'isws_facility_id': str})

for row in df.iterrows():
    if pd.isnull(row[1][5]) or pd.isnull(row[1][6]):
        df.drop(row[0], inplace = True)
        

df.reset_index(inplace = True, drop = True)

for row in df.iterrows():
    if pd.isnull(row[1][7:]).all():
        df.drop(row[0], inplace = True)
        
df.reset_index(inplace = True, drop = True)

trans_df = df.transpose()

df2 = trans_df.iloc[7:].astype('float').interpolate(limit_area = 'inside')

for column in df2:

    if not pd.isna(df2[column]['2012':]).any():
        df2[column]['2012':] = df2[column]['2012':].fillna(method='ffill')
        
    if df2[column].isnull().all():
        df2.drop(column, axis = 1, inplace = True)
        
#df2 = df2.transpose()