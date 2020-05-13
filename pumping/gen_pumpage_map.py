# -*- coding: utf-8 -*-
"""
Created on Tue May 12 18:45:17 2020

@author: iordach1
"""

import cartopy
import pyproj
import pandas as pd



#----------------------------------------------------------------------------
'''GRL'''
sw_lat =  41.3 #southwest latitude
sw_long = -90.5 #southwest longitude
ne_lat =  41.9 #northeast latitude
ne_long = -89.4 #northeast longitude

illimap = {'proj': 'lcc', # Lambert Conformal Conic
     'ellps': 'clrk66',
     'lon_0': -89.5,
     'lat_0': 33,
     'lat_1': 33,
     'lat_2': 45,
     'x_0': 2999994,
     'y_0': 0}

wgs_84 = {'proj': 'longlat'
,
'datum': 'WGS84'
,
'no_defs': True}
         
prj = pyproj.Proj(illimap)

wgs84 = pyproj.Proj(wgs_84)

nex, ney = pyproj.transform(wgs84,prj,ne_long,ne_lat)
swx, swy = pyproj.transform(wgs84,prj,sw_long,sw_lat)


df = pd.read_csv('processPumpData.csv')

coords = df[['x','y']]

for row in coords.iterrows():
    print(pyproj.transform(prj,wgs84,row[1][0], row[1][1]))

#nex, ney = round(row[1][0]/0.3048,-4), round(row[1][1]/0.3048,-4)
#swx, swy = round(swx/0.3048,-4), round(swy/0.3048,-4)

