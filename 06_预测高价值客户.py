import os
import numpy as np
import pandas as pd

# from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression

# 读取数据
df_tl = pd.read_csv("./output/time_line.csv", encoding='utf8')
df_ids = pd.read_csv("./output/ids.csv", encoding='utf8')
ids = df_ids['id']
# date_range_min = df_tl['date_num'].min()
# date_range_max = df_tl['date_num'].max()
print(df_tl[''])


# 开始训练
# lg = LogisticRegression(solver='lbfgs', multi_class='auto')
# lg.fit(feature, target)
# # print("K值", lg.coef_)

