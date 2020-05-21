import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.interpolate as spi
from zhmh import get_path

import statsmodels
import statsmodels.api as sm
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf


# 参数设置
DEBUG = False
PREDICT_DAYS = 30


# 读取数据
ids = pd.read_csv("./output/ids.csv")['id']
df = pd.read_csv(
    "./output/time_sequence.csv",
    dtype={'id': np.int32, 'fee': np.float64, 'days': np.int32},
    parse_dates=['date']
)
DATE_BOUND = {
    'min': df['date'].min(),
    'max': df['date'].max(),
    'min_d': df['days'].min(),
    'max_d': df['days'].max(),
}
DATE_BOUND['length'] = DATE_BOUND['max_d'] - DATE_BOUND['min_d'] + 1
DATE_RANG = pd.period_range(DATE_BOUND['min'], DATE_BOUND['max'], freq='D')
DATE_DAYS_RANG = range(DATE_BOUND['min_d'], DATE_BOUND['max_d'] + 1)


index = 1
# 循环训练
for uid in ids:
    # if uid != 1000000092: continue
    print(uid)
    pre_data = df[df['id'] == uid]
    # print(pre_data)

    range_min = int(pre_data['days'].min())
    range_max = int(pre_data['days'].max())
    # range_drop = int((range_max - range_min + 1) * 0)
    # range_min += range_drop
    # range_max -= range_drop
    param_x, param_y = list(pre_data['days']), list(pre_data['fee'])

    ##############################

    # 插值处理
    # ipf = spi.UnivariateSpline(param_x, param_y)
    ipf = spi.interp1d(param_x, param_y, kind='quadratic')

    ##############################

    # 统计插值
    days = range(range_min, range_max)
    fee = []
    for i in days:
        fee.append(ipf(i))
    data = pd.DataFrame(data={'fee': fee})
    data['fee'] = data['fee'].astype('float32')
    data.index = days
    data.index.name = None

    ##############################

    # 绘图
    plt.subplot(221)
    plt.plot(pre_data['days'], pre_data['fee'], label='Origin')
    plt.plot(days, fee, label='Interpolation')
    plt.grid()
    plt.title('Interpolation')
    plt.legend()
    # plt.show()

    ##############################

    # # 差分
    data_diff = data.diff(1).dropna()

    # ACF
    plot_acf(data_diff, ax=plt.subplot(223))

    # PACF
    plot_pacf(data_diff, ax=plt.subplot(224))

    ##############################

    try:
        arima = ARIMA(data, order=(1, 2, 1))
        result = arima.fit(disp=False)
    except ValueError:
        # plt.show()
        arima = ARIMA(data, order=(2, 2, 1))
        result = arima.fit(disp=False)
    # end try

    # print(result.aic, result.bic, result.hqic)
    plt.subplot(222)
    plt.plot(data_diff, label='Diff')
    plt.plot(result.fittedvalues, label='ARIMA')
    plt.title('ARIMA')
    plt.grid()
    plt.legend()
    if DEBUG:
        plt.show()
        break
    else:
        plt.savefig(get_path('./output/plt', uid))
        plt.close()
    # end if
    index += 1

