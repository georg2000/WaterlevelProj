import pandas as pd
import Conv_Niederschlag
import Conv_Wasserstand
import matplotlib.pyplot as plt
import statsmodels.api as sm
from IPython.display import display

def create_df_shift(stations_list, lag, colname, path_pr_first ):

    stt = []
    for n in stations_list:
        p = path_pr_first.replace(stations_list[0], n)
        stt.append(p)
        #print("st:",st)

    # stt = []
    # x = 0
    # for n in st:
    #     p = n.replace(order_list[0], order_list[x])
    #     print(p)
    #     stt.append(p)
    #     x += 1
    # print(stt)


    df_end = Conv_Niederschlag.convert_precip(path_pr_first, colname, "days")[1]
    #df_fin = df_end.join(df, how='outer', lsuffix="fuck", rsuffix="shit")
    count_path = 0
    for path in stt:
        df = Conv_Niederschlag.convert_precip(path, colname, "days")[1]
        #print("df:", df, path)

        count_lag = 0
        while count_lag <= lag:
            #print(count_path)
            df["lag"+str(count_lag)+stations_list[count_path]] = df[colname].shift(count_lag)
            count_lag += 1
        df = df.drop(colname, axis=1)
        #df = df.rename(columns={colname: "lag" + str(count_lag-lag-1) + stations_list[count_path]})
        #df = df.drop(df.columns[2], axis=1)
        count_path += 1
        df_end = df_end.join(df, how='outer')

    df_end = df_end.drop(columns=[colname], axis=0)
    df_end = df_end.dropna()
    #print(df_end)
    return df_end

#df = create_df_shift(["MOE"], 6, "rre150d0", "Data_Precipitation/Precip_1990-2020_day_all/order_MOE_rre150d0_1_data.txt")
#print(df)
#df.to_csv("MOE_Lag6.csv")


