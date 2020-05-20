import numpy as np
import pandas as pd

# 读取数据
df_pay = pd.read_csv("./customer_pay_habbit.csv", encoding='utf8')
df_pay.columns = ['id', 'date', 'fee']

# 读取用户ID表
df_ids = pd.read_csv("./output/ids.csv", encoding='utf8')
ids = df_ids['id']

# Buffer
user_buffer = []

for uid in ids:
    lines = df_pay[df_pay['id'] == uid]
    col_date = lines['date']
    col_fee = lines['fee']
    print(col_date)
    user_buffer.append({
        'id': uid,
        'pay_times': col_fee.shape[0],
        'pay_sum': col_fee.sum(),
        'pay_mean': col_fee.mean()
    })

df_user = pd.DataFrame(user_buffer)
df_user.to_csv("./output/user.csv", index=False, encoding='utf-8-sig')
