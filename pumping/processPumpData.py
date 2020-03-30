# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 14:48:57 2020

@author: iordach1
"""

import pandas as pd

input_file = "Pumpage_Data_GRL.csv"

df = pd.read_csv(input_file, dtype = {'isws_facility_id': str})

pivot_df = 