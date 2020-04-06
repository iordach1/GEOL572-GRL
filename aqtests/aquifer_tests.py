# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 17:45:45 2020

@author: Anthony Groenewold
"""

#%%
# Import all necessary packages
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as spo
import scipy.special as sps
import math

#%%
# Aquifer Test for Sankoty Aquifer

# This test was conducted in Princeton, IL

# Import aquifer test data from the Excel spreadsheet
sankoty_df=pd.read_excel("https://github.com/iordach1/GEOL572-GRL/blob/develop/aqtests/Princeton.xlsx?raw=true",index_col=0)

#Plot drawdown versus time
sankoty_df.plot(style="o",legend=None)
plt.xlabel("Time (min)")
plt.ylabel("Drawdown (ft)")
plt.title("Sankoty aquifer test: observed data")
plt.show()

#Plot drawdown versus time with the x-axis on a logarithmic scale
plt.semilogx(sankoty_df,"o")
plt.xlabel("Time (min)")
plt.ylabel("Drawdown (ft)")
plt.title("Sankoty aquifer test: observed data")
plt.ylim(8,10)
plt.show()

# Define parameters
#Note that for the data used here, the test well doubled as the observation well
r = 8/12 #Radius of the screen in the test well; ft
b = 100 #Average aquifer thickness; ft
Q = 1200*192.5/(24*60) #Pumping rate; ft^3/min

#Crop the dataset to contain a subset of data points.  The Theis curve will be fit to this subset.
#sankoty_subset=sankoty_df["drawdown_ft"][2:5] #This was the subset of data points used in the 1980 test, but returns a storage coefficient that is very low.
sankoty_subset=sankoty_df["drawdown_ft"][9:13] #This subset of data is also linear and returns a slightly more realistic storage coefficient

#Define a function based on the Theis equation to fit to the observed data
def Theis(t,S,T):
  u=(r**2*S)/(4*T*t) #This will be the argument of the well function, also known as the exponential integral
  return Q/(4*math.pi*T)*sps.exp1(u)

#Fit the "theis" function, defined above, to the chosen subset of data ("sankoty_subset")
popt,pcov=spo.curve_fit(Theis,sankoty_subset.index,sankoty_subset,p0=[10**-9,10**-9])
#popt is a list containing the storage coefficient (S) and the transmissivity (T)
#S is located at popt[0]; it is unitless
#T is located at popt[1]; it has units of ft^2/min

#Create lists of the x and y points of the fitted Theis curve, for plotting purposes
xx=[value for value in sankoty_subset.index] #x values (time in minutes to be plotted)
u=[] #Empty list for u values, to be used with the "Theis" function
yy=[] #Empty list for y values, to be overwritten by outputs from the "Theis" function
for value in xx:
  u.append((r**2*popt[0])/(4*popt[1]*value))
  yy.append(Theis(value,popt[0],popt[1]))

popt[1]=popt[1]*60*24 #Convert transmissivity from ft^2/min to ft^2/d

#Plot the observed data and the fitted Theis curve together.
plt.semilogx(sankoty_subset,"o",xx,yy)
plt.xlabel("Time (min)")
plt.ylabel("Drawdown (ft)")
plt.title("Sankoty aquifer test: observed drawdown with fitted Theis solution")
plt.show()

print('The storage coefficient S is found to be '+str(round(popt[0],8))+'.')
print('The transmissivity T is found to be '+str(int(round(popt[1])))+' ft^2/d.')

#S should be between 10^-5 and 10^-3 (roughly)

#%%
# Aquifer Test for Tampico Aquifer

# This test was conducted in Sterling, IL

#Import aquifer test data from the Excel spreadsheet
tampico_df=pd.read_excel("https://github.com/iordach1/GEOL572-GRL/blob/develop/aqtests/Sterling.xlsx?raw=true",index_col=0)

#Plot drawdown versus time
tampico_df.drawdown_ft.plot(style="o",legend=None)
plt.xlabel("Time (min)")
plt.ylabel("Drawdown (ft)")
plt.title("Tampico aquifer test: observed data")
plt.show()

#Plot drawdown versus time with the x-axis on a logarithmic scale
plt.semilogx(tampico_df.drawdown_ft,"o")
plt.xlabel("Time (min)")
plt.ylabel("Drawdown (ft)")
plt.title("Tampico aquifer test: observed data")
plt.ylim(3,7)
plt.show()

# Define parameters
#Note that for this aquifer test, the test well doubled as the observation well
r = 10/12 #Radius of the screen in the test well; ft
b = 40 #Average aquifer thickness; ft
Q = 863*192.5/(24*60) #Pumping rate; ft^3/min

#Note that in this aquifer test, the pumping rate was less than Q for about 90 minutes.
#From t=95 min. onward, the pumping rate was Q.
#Data points before t=95 min may need to be neglected when fitting the Theis curve to the data.

#Crop the dataset to contain a subset of data points.  The Theis curve will be fit to this subset.
tampico_subset=tampico_df["drawdown_ft"][2:6] #This was the subset of data points used in the 1962 aquifer test

#Fit the "theis" function, defined in the previous code block, to the chosen subset of data ("tampico_subset")
popt,pcov=spo.curve_fit(Theis,tampico_subset.index,tampico_subset,p0=[10**-9,10**-9])
#popt is a list containing the storage coefficient (S) and the transmissivity (T)
#S is located at popt[0]; it is unitless
#T is located at popt[1]; it has units of ft^2/min

#Create lists of the x and y points of the fitted Theis curve, for plotting purposes
xx=[value for value in tampico_subset.index] #x values (time in minutes to be plotted)
u=[] #Empty list for u values, to be used with the "Theis" function
yy=[] #Empty list for y values, to be overwritten by outputs from the "Theis" function
for value in xx:
  u.append((r**2*popt[0])/(4*popt[1]*value))
  yy.append(Theis(value,popt[0],popt[1]))

popt[1]=popt[1]*60*24 #Convert transmissivity from ft^2/min to ft^2/d

#Plot the observed data and the fitted Theis curve together.
plt.semilogx(tampico_subset,"o",xx,yy)
plt.xlabel("Time (min)")
plt.ylabel("Drawdown (ft)")
plt.title("Sankoty aquifer test: observed drawdown with fitted Theis solution")
plt.show()

print('The storage coefficient S is found to be '+str(round(popt[0],20))+'.')
print('The transmissivity T is found to be '+str(int(round(popt[1])))+' ft^2/d.')

#S should be between 0.05 and 0.3 (roughly)