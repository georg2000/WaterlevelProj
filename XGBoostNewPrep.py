#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 00:51:59 2022

@author: geo
"""

import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import numpy as np
import math
import Conv_Niederschlag
import Conv_Wasserstand
import Import_Waterlevel
import matplotlib.pyplot as plt
import statsmodels.api as sm
import Create_lag_df
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectFromModel
import pickle
from IPython.display import display


#Here the best set of precipitation measurement stations is givan but could be changed, as well as lag.
df = Import_Waterlevel.data_lag
print("dfn:\n", df)

df_waterlts = Conv_Wasserstand.convert_waterlevel("Data_Waterlevel/2116_Pegel_Stundenmittel_1974-01-01_2020-03-01.csv", "days")[1]


#time frame func for ts
def datex(df,date_start, date_end): #format 'yyyy-mm-dd'
    maskx = (df.index > date_start) & (df.index <= date_end)
    return df.loc[maskx]


#split train and test set by date
Ytrain= datex(df_waterlts,'2011-03-12', '2018-12-30')
Xtrain= datex(df,'2011-03-12', '2018-12-30')
Xtest = datex(df,'2019-01-01', '2020-03-01')
Ytest = datex(df_waterlts,'2019-01-01', '2020-03-01')

# print(Xtrain)
# print(Ytrain)
#now we try to fit a linReg for the chosen frame
X_train = Xtrain.iloc[:].reset_index(drop=True)
X_test = Xtest.iloc[:].reset_index(drop=True)
Y_train = Ytrain.Wert.reset_index(drop=True)
Y_test = Ytest.Wert.reset_index(drop=True)

Xtrain.head()
print(X_test)


#prepare regressor
xg_reg = xgb.XGBRegressor()

# Fit the regressor to the training set with fit()
xg_reg.fit(X_train,Y_train)
xg_reg.fit(X_train,Y_train)

# Make predictions to the test set with predict()
Y_pred = xg_reg.predict(X_test)

#safe model
pickle.dump(xg_reg, open("modelXG.sav", 'wb'))

# Compute the rmse from sklearns metrics module imported earlier
rmse = np.sqrt(mean_squared_error(Y_test, Y_pred))
print("RMSE: %f" % (rmse))

#prepare for time series plot
index = pd.date_range(start=pd.Timestamp('2019-01-02'), end=pd.Timestamp('2020-03-01'))
timeindex = pd.DatetimeIndex(index)
df = pd.DataFrame(data=Y_pred, columns=['waterlevel'])
df = df.set_index(timeindex)


#plot timeseries precipitation
fig, axs = plt.subplots(2)
fig.suptitle('Time Series of real water levels vs. predicted')
axs[0].plot(Ytest.index, Ytest.Wert)
axs[1].plot(df.index, df.waterlevel)
plt.show()