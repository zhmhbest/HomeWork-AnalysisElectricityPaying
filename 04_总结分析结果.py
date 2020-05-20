import numpy as np
import pandas as pd

# 读取数据
# df_pay = pd.read_csv("./customer_pay_habbit.csv")
df_ids = pd.read_csv("./output/ids.csv")
ids = df_ids['id']
df_plus = pd.read_csv("./output/user_plus.csv")

# 用户类型
"""
    0: '高价',
    1: '潜力',
    2: '大众',
    3: '低价'
"""

# Summary
type_0 = df_plus[0 == df_plus['type']]
type_1 = df_plus[1 == df_plus['type']]
type_2 = df_plus[2 == df_plus['type']]
type_3 = df_plus[3 == df_plus['type']]
# row_size = max(type_0.shape[0], type_1.shape[0], type_2.shape[0], type_3.shape[0])

type_id_0 = type_0['id'].reset_index(drop=True, inplace=False)
type_id_1 = type_1['id'].reset_index(drop=True, inplace=False)
type_id_2 = type_2['id'].reset_index(drop=True, inplace=False)
type_id_3 = type_3['id'].reset_index(drop=True, inplace=False)

# 合成DF
df_summary = pd.DataFrame()
df_summary['高价值型'] = type_id_0.astype("object")
df_summary['潜力型'] = type_id_1.astype("object")
df_summary['大众型'] = type_id_2.astype("object")
df_summary['低价值型'] = type_id_3.astype("object")
# print(df_summary)
df_summary.to_csv("./output/summary.csv", index=False, encoding='utf-8-sig')
