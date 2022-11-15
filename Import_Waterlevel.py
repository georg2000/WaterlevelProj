#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 00:44:02 2022

Processing new data

@author: geo
"""

import pandas as pd

pd.set_option('display.max_columns', None)
#import data
df = pd.read_csv("Data_Precipitation/dataP.csv", encoding="latin_1", sep=";")

#check for Nan values
df.isnull().values.any()
df = df.fillna(0)
#change col name
df = df.rename(columns={'ï»¿Datum':'Date'})
#this will truncate the column name. Then print the dataframe
df.rename(columns=lambda x: x[:5], inplace=True) 

print(df)
df.size
df.isnull().values.any()
#Achtung bis hier stimmt die Anzahl Tage noch


#check data format and change date format
print(df.dtypes)
df['Date']= pd.to_datetime(df.Date, format="%d.%m.%Y")
df = df.set_index("Date")

print(df)
print(list(df))
df.size

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
    #gf = pd.concat([gf,ef], axis=1)
    gf = gf.join(ef, how='outer')
    #print(gf)
print(gf)
#gf.insert(loc=0, column= 'Date', value=df['Date'])
data_lag = gf.dropna()
#data_lag = gf.set_index("Date")

print(data_lag)

#df = df.drop(colname, axis=1)
        #df = df.rename(columns={colname: "lag" + str(count_lag-lag-1) + stations_list[count_path]})
        #df = df.drop(df.columns[2], axis=1)
#count_path += 1
#df_end = df_end.join(df, how='outer')
#print(ef)
#print(df)

