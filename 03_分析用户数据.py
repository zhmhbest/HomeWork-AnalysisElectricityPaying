import numpy as np
import pandas as pd

# 读取数据
df_ids = pd.read_csv("./output/ids.csv")
ids = df_ids['id']
df_user = pd.read_csv("./output/user.csv")
df_mean = pd.read_csv("./output/user_mean.csv")
mean_times = df_mean.head(1)['times'].values[0]
mean_pay = df_mean.head(1)['pay'].values[0]
print("人均缴费次数：", mean_times)
print("次均缴费额度：", mean_pay)

# 定义用户类型
USER_TYPE = {
    '高价': 0,
    '潜力': 1,
    '大众': 2,
    '低价': 3
}

# Buffer
user_buffer = []

for uid in ids:
    line = df_user[df_user['id'] == uid]
    # print(line)

    if line['pay_times'].item() < mean_times:
        # 潜力 低价
        if line['pay_mean'].item() > mean_pay:
            user_buffer.append(USER_TYPE['潜力'])
        else:
            user_buffer.append(USER_TYPE['低价'])
    else:
        # 高价 大众
        if line['pay_mean'].item() > mean_pay:
            user_buffer.append(USER_TYPE['高价'])
        else:
            user_buffer.append(USER_TYPE['大众'])
    # end if


# 追加一列
df_user['type'] = user_buffer
df_user.to_csv("./output/user_plus.csv", index=False, encoding='utf-8-sig')
