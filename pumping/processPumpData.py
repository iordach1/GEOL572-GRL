# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 14:48:57 2020

@author: iordach1
"""

import pandas as pd
import json
#import matplotlib.pyplot as plt

#%%user functions
def estimate_irr_acIN(acres, inches):   return acres * inches * 27000
def estimate_irr_galAcre(acres):    return 325000 * acres
def gpa_to_cfd(gpa): return -(gpa * 0.133681)/365.25

#%%read in data
input_file_IWIP = "Pumpage_Data_GRL.csv"
input_file_agIRR = "centerpivot2014.csv"

IWIP_df = pd.read_csv(input_file_IWIP, dtype = {'isws_facility_id': str, 'p_num': str})

agIRR_df = pd.read_csv(input_file_agIRR, header=0, names = ['AREA_ACRES', 'x', 'y', 'yr'] )
agIRR_df['wellID'] = agIRR_df.index
agIRR_df['wellID'] = agIRR_df['wellID'].apply(lambda x: "i_{0:06d}".format(x))
agIRR_df['z'] = -999
#agIRR_df['Q'] = estimate_irr_acIN(agIRR_df['AREA_ACRES'], 30*12)
agIRR_df['Q'] = estimate_irr_galAcre(agIRR_df['AREA_ACRES'])

static_df = IWIP_df.copy(deep = 'True')

#%%clean data
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

trans_df = IWIP_df.transpose()

IWIP_df2 = trans_df.iloc[7:].astype('float').interpolate(limit_area = 'inside')
print("Interpolated between data gaps")

for column in IWIP_df2:
    for i in range(2012,2020):
        if not pd.isna(IWIP_df2[column][str(i)]):
            IWIP_df2[column][str(i):] = IWIP_df2[column][str(i):].fillna(method='ffill')
print("Forward fill last 7 years of data")
        
IWIP_df.iloc[:,7:] = IWIP_df2.transpose()

IWIP_df.to_csv("Pumpage_Data_GRL_mod.csv")

#%%output to flopy format
iwip_rename_dict = {list(IWIP_df.columns)[0]: 'wellID',
                    list(IWIP_df.columns)[5]: 'x',
                    list(IWIP_df.columns)[6]: 'y',
                    list(IWIP_df.columns)[4]: 'z',
                    list(IWIP_df.columns)[len(IWIP_df.columns)-1]: 'Q'}

out_df = IWIP_df.iloc[:, [0,5,6,4,len(IWIP_df.columns)-1]].rename(columns = iwip_rename_dict)
out_df = out_df.append(agIRR_df.iloc[:, [4,1,2,5,6]], ignore_index = True)
out_df['Q'] = gpa_to_cfd(out_df['Q'])

#csv
out_df.to_csv("processPumpData.csv")
print("exported processed data to csv")

lrcq = {0:[]}
for row in out_df.iterrows():
    lrcq[0].append(list(row[1][[3,2,1,4]]))
    
js_pump = json.dumps(lrcq, indent = 4)

#json
with open("processPumpData.json", "w") as outfile: 
    outfile.write(js_pump)
print("exported processed data to json")

#%%plots


# for row in IWIP_df.sample(5).iterrows():
#     plt.figure(figsize=(17,11))
#     plt.plot([x for x in range(1981, 2019)], row[1][7:], '--', label = 'mod', linewidth =3)
#     plt.plot([x for x in range(1981, 2019)], static_df[static_df['p_num'] == row[1][0]].iloc[:,7:].values.tolist()[0], label = 'orig', linewidth = 3)
#     plt.title("Well p_num: {0}".format(row[1][0]))
#     plt.xlim(1981, 2018)
#     plt.legend()
#     plt.savefig("{0}.jpg".format(row[1][0]))
#     plt.clf()
    

    