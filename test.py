import Conv_Niederschlag
import Conv_Wasserstand
import Create_lag_df

dff = Conv_Niederschlag.convert_precip("Data_Precipitation/Precip_1990-2020_day_all/order_AFI_rre150d0_1_data.txt","rre150d0","days" )[1]

df = Create_lag_df.create_df_shift(['ARI'], 6, "rre150d0", "Data_Precipitation/Precip_1990-2020_day_all/order_AFI_rre150d0_1_data.txt")

df_waterlts = Conv_Wasserstand.convert_waterlevel("Data_Waterlevel/2289_Pegel_Stundenmittel_1974-01-01_2020-03-01.csv", "days")[1]


#time frame func for ts
def datex(df,date_start, date_end): #format 'yyyy-mm-dd'
    maskx = (df.index > date_start) & (df.index <= date_end)
    return df.loc[maskx]

df_ts_wl = datex(df_waterlts,'1992-02-01', '2019-11-01')
df_tf = datex(df,'1992-02-01', '2019-11-01')
df_tff = datex(dff,'1992-02-01', '2019-11-01')

print(df_tf)
print(df_tff)