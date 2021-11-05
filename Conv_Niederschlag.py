#!/usr/bin/env python
# coding: utf-8

import pandas as pd

def convert_precip(path, colname, d): #example:'Data_Precipitation/Precip_BS-BL_1990-2020/order_85490_ARI_rre150d0_1_data.txt'
                                      #d is "hours" for data with hours and "days" if only with days
    df = pd.read_csv(path, encoding="latin_1", sep=";")


    #if the data is mxed with different Stations use this:
    #df = df[df['stn']=="BAS"]

    #summary
    #print("df summary:\n", df.describe())
    #print("shape df:\n",df.shape)
    #print("df types:\n",df.dtypes)
    #print("df:\n",df)


    #check for Nan values
    df.isnull().values.any()
    #print("\nNan count:",df.isnull().sum().sum())

    #check for "_" values exchange with 0
    df.loc[(df[colname] == '-'),colname ]=0


    #change data dtypes
    df[colname] = df[colname].astype("float")
    #df1.time = df1.time.astype("string")


    #change dtype to_datetime
    if d == "hours":
        df.time = pd.to_datetime(df['time'], format='%Y%m%d%H').copy()
        #print("\ndf types new:\n",df.dtypes)
    if d == "days":
        df.time = pd.to_datetime(df['time'], format='%Y%m%d').copy()
        #print("\ndf types new:\n",df.dtypes)


    #extract columns, here dff is with index for LinReg models
    dff = df[['time', colname]]
    #print("dff:\n",dff)

    #create time series, with date as time
    df_timeindex = df.set_index(df['time'])
    df_timeindex.drop(['time'], axis=1,inplace=True)
    df_timeindex.drop(["stn"], axis=1, inplace=True)
    #print(df_timeindex.head())

    return dff, df_timeindex

#d,t = convert_precip("Data_Precipitation/Precip_BS-BL_1990-2020/order_85490_REG_rre150d0_1_data.txt")