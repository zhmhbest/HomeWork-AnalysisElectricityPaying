import numpy as np
import pandas as pd

# 读取数据
# df_pay = pd.read_csv("./customer_pay_habbit.csv", encoding='utf8')
df_ids = pd.read_csv("./output/ids.csv", encoding='utf8')
ids = df_ids['id']
df_usr = pd.read_csv("./output/user.csv", encoding='utf8')

# 定义用户类型
USER_TYPE = {
    '高价': 0,
    '潜力': 1,
    '大众': 2,
    '低价': 3
}

# 计算平均付费能力
user_number = df_usr.shape[0]
all_times = df_usr['pay_times'].sum()
all_fee = df_usr['pay_sum'].sum()
mean_times = all_times / user_number    # 人均缴费次数
mean_pay = all_fee / all_times          # 次均缴费额度
print("人均缴费次数：", mean_times)
print("次均缴费额度：", mean_pay)

# Buffer
user_buffer = []

for uid in ids:
    line = df_usr[df_usr['id'] == uid]
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
df_usr['type'] = user_buffer
df_usr.to_csv("./output/user_plus.csv", index=False, encoding='utf-8-sig')
