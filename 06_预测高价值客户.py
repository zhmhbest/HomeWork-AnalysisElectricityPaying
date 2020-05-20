import numpy as np
import pandas as pd

# 读取数据
df_tl = pd.read_csv("./output/time_line.csv", encoding='utf8')
df_tl['date'] = df_tl['date'].astype('datetime64')
df_ids = pd.read_csv("./output/ids.csv", encoding='utf8')
ids = df_ids['id']

# pd.DatetimeIndex()
print(df_tl)
