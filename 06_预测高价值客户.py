import os
import numpy as np
import pandas as pd
import statsmodels
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy import stats

# 参数设置
PREDICT_TIME = 7

# 读取数据
ids = pd.read_csv("./output/ids.csv")['id']
df = pd.read_csv("./output/time_sequence.csv", parse_dates=['date'])
# di = pd.DatetimeIndex(df['date'])


def paint_user(uid, user_data, save_path=''):
    def common_paint():
        plt.title(uid)
        plt.plot(user_data['date'], user_data['fee'])
        plt.grid(True)
    if 0 == save_path.__len__():
        common_paint()
        plt.show()
        plt.close()
    else:
        save_path = os.path.abspath(os.path.join(save_path, str(uid) + '.png'))
        if os.path.exists(save_path):
            return
        # end if
        print(save_path)
        common_paint()
        plt.savefig(save_path, format='png')
        plt.close()


for uid in ids:
    print(uid)
    lines = df[df['id'] == uid]
    # 绘制用户付费图
    paint_user(uid, lines, './output/plt')
