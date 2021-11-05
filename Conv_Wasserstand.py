#!/usr/bin/env python
# coding: utf-8



import pandas as pd


def convert_waterlevel(path, aggregation):
#path example: "Data_Proto/2289_Pegel_Stundenmittel_1974-01-01_2020-03-01.csv"
#aggregation: hours or days
    df = pd.read_csv(path, sep=";",header = 8, encoding="latin_1")


#Get an overview
#print("shape df:\n", df.shape)
#print("info df:\n",df.info())
#print("df:\n",df)

    #change oject to string and test values if numeric
    df.Wert = df.Wert.astype("str")
    df.Wert.str.replace(".","")


    #get rid of all nonnumeric rows and more formatting
    bool = df.Wert.str.replace(".","").str.isnumeric()
    df1 = df[bool==True]
    df1.Wert = df1.Wert.astype("float")
    #df1['Wert'].max()


    #conv Zeitstempel to daytime
    df1['Zeitstempel'] = pd.to_datetime(df1.Zeitstempel)


    #print("shape df:\n",df.shape)
    #print("shape df1:\n",df1.shape)



    #print("df1:\n",df1)
    #df1.describe()

    #eig df2
    df3 = df1[['Zeitstempel','Wert']]
    #print("df2:\n",df3)

    if aggregation == "days":
        #aggregate to daily mean
        df3 = df3.groupby(df3['Zeitstempel'].dt.date).mean().reset_index()
        #print(df3.dtypes)
        #print("df3:\n",df3)


    #conv Zeitstempel to daytime
    df3['Zeitstempel'] = pd.to_datetime(df3.Zeitstempel)
    #print(df3.dtypes)

    #create time series, with date as time
    df3_timeindex = df3.set_index(df3['Zeitstempel'])
    df3_timeindex.drop(['Zeitstempel'], axis=1,inplace=True)
    #print(df3_timeindex.head())
    return df3, df3_timeindex