import numpy as np
import pandas as pd

# 读取数据
df_pay = pd.read_csv("./customer_pay_habbit.csv")
df_pay.columns = ['id', 'date', 'fee']

# 读取用户ID表
df_ids = pd.read_csv("./output/ids.csv")
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


# 保存
df_user = pd.DataFrame(user_buffer)
df_user.to_csv("./output/user.csv", index=False, encoding='utf-8-sig')


# 计算平均付费能力
user_number = df_user.shape[0]
all_times = df_user['pay_times'].sum()
all_fee = df_user['pay_sum'].sum()
mean_times = all_times / user_number    # 人均缴费次数
mean_pay = all_fee / all_times          # 次均缴费额度
pd.DataFrame({
    "times": [mean_times],
    "pay": [mean_pay]
}).to_csv("./output/user_mean.csv", index=False, encoding='utf-8-sig')
print("人均缴费次数：", mean_times)
print("次均缴费额度：", mean_pay)
