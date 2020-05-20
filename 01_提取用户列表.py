import numpy as np
import pandas as pd


df_pay = pd.read_csv("./customer_pay_habbit.csv")

# 修改列名
df_pay.columns = ['id', 'date', 'fee']

# 选择ID列
col_id = df_pay['id']
print(col_id.dtype)

# 去除重复
view_ids = col_id.drop_duplicates()

# 深拷贝+重建索引
# ids = view_ids.reset_index(drop=True, inplace=False)

# 保存
view_ids.to_csv("./output/ids.csv", index=False, encoding='utf-8-sig')
