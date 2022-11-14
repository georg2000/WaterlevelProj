#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 00:44:02 2022

Processing new data

@author: geo
"""
from IPython.display import display
import pandas as pd

pd.set_option('display.max_columns', None)
#import data
df = pd.read_csv("Data_Precipitation/dataP.csv", encoding="latin_1", sep=";")

#check for Nan values
df.isnull().values.any()

#change col name
df = df.rename(columns={'ï»¿Datum':'Date'})
#this will truncate the column name. Then print the dataframe
df.rename(columns=lambda x: x[:5], inplace=True) 
print(df)

#check data format and change date format
print(df.dtypes)
df['Date']= pd.to_datetime(df.Date)


print(list(df))

gf = pd.DataFrame()
#perform lag
for n in list(df)[1:]:

    
    lag = 3
    count_lag = 0
    colname = 1
    ef = pd.DataFrame()
    
    while count_lag <= lag:
        #print(df)
        ef[n+"lag"+str(count_lag)] = df[n].shift(count_lag)
        #print(ef)
        #df.insert(loc=count_lag+1, column= n +"lag"+str(count_lag), value=ef.iloc[:,count_lag])
        count_lag += 1
        colname += 1
    print(ef)
    gf = pd.concat([gf,ef], axis=1)
    #print(gf)

gf.insert(loc=0, column= 'Date', value=df['Date'])
gf = gf.dropna()
gf = gf.set_index("Date")
print(gf)
#df = df.drop(colname, axis=1)
        #df = df.rename(columns={colname: "lag" + str(count_lag-lag-1) + stations_list[count_path]})
        #df = df.drop(df.columns[2], axis=1)
#count_path += 1
#df_end = df_end.join(df, how='outer')
#print(ef)
#print(df)

