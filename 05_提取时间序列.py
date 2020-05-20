import numpy as np
import pandas as pd


def get_date_from_string(sda):
    import datetime
    """
    从字符串创建一个date对象
    :param {string} sda:
    """
    s = sda.split('-')
    return datetime.date(int(s[0]), int(s[1]), int(s[2]))


# 读取数据
df_pay = pd.read_csv("./customer_pay_habbit.csv", encoding='utf8')
df_pay.columns = ['id', 'date', 'fee']
df_ids = pd.read_csv("./output/ids.csv", encoding='utf8')
ids = df_ids['id']

# 修正日期列
df_pay['date'] = df_pay['date'].astype('datetime64')

# 按时间排序
df_pay.sort_values(by='date', inplace=True)

# 重建索引
df_pay.reset_index(drop=True, inplace=True)

# 日期整数化
first_date = df_pay.loc[0]['date']
df_pay['date_num'] = df_pay['date'].map(lambda x: (x - first_date).days)

# 保存
df_pay.to_csv("./output/time_line.csv", index=False, encoding='utf-8-sig')
