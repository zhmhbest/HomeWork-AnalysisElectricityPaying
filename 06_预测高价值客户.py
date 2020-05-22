import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.interpolate as spi
from zhmh import get_path
from statsmodels.tsa.arima_model import ARIMA, ARMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf


# 参数设置
SUB_PADDING = 1.5  # 子图间距
DEBUG = False
DEBUG_NUM = 3
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

    ##############################

    # 数据准备
    print(uid, end=': ')
    pre_data = df[df['id'] == uid]
    # print(pre_data)
    first_data = pre_data.head(1)
    first_date = first_data['date'].values[0]
    first_fee = first_data['fee'].values[0]
    # print('date:', first_date)
    # print('fee:', first_fee)

    ##############################

    # 范围
    range_days_min, range_days_max = int(pre_data['days'].min()), int(pre_data['days'].max())
    range_days = range(range_days_min, range_days_max + 1)
    print(range_days_min, range_days_max)
    range_date_min, range_date_max = pre_data['date'].min(), pre_data['date'].max()
    range_date = pd.period_range(range_date_min, range_date_max, freq='D')
    print(range_date_min, range_date_max)

    ##############################

    # 插值处理
    param_x, param_y = list(pre_data['days']), list(pre_data['fee'])
    # ipf = spi.UnivariateSpline(param_x, param_y)
    ipf = spi.interp1d(param_x, param_y, kind='quadratic')

    # 统计插值
    fee = []
    for i in range_days:
        fee.append(ipf(i))
    data = pd.DataFrame(data={'fee': fee})
    data['fee'] = data['fee'].astype('float32')
    data.index = range_date
    data.index.name = None
    # print(data)

    ##############################

    # 绘图
    plt.subplot(221)
    plt.plot(pre_data['days'], pre_data['fee'], label='Origin')
    plt.plot(range_days, fee, label='Interpolation')
    plt.grid()
    plt.title('Interpolation')
    plt.legend()
    # plt.show()

    ##############################

    # 差分
    data_diff = data.diff(1).dropna()
    diff_first_data = data_diff.head(1)
    diff_first_date = diff_first_data.index.values[0]
    diff_first_fee = diff_first_data['fee'].values[0]

    # ACF
    plot_acf(data_diff, ax=plt.subplot(223))

    # PACF
    plot_pacf(data_diff, ax=plt.subplot(224), method='ywm')
    # plt.show()
    # break

    ##############################

    # 创建模型
    # https://www.statsmodels.org/devel/generated/statsmodels.tsa.arima_model.ARIMA
    try:
        ts_module = ARIMA(data_diff, order=(2, 1, 1)).fit(disp=False)
    except ValueError:
        print("err", uid)
        break
    # end try
    fitted_values = ts_module.fittedvalues
    # print(module.aic, module.bic, module.hqic)

    ##############################

    # 绘图
    plt.subplot(222)
    plt.plot(data_diff.index, data_diff['fee'], label='Diff')
    plt.plot(fitted_values.index, fitted_values, label='ARIMA')
    plt.title('ARIMA')
    plt.grid()
    plt.legend()
    plt.tight_layout(SUB_PADDING)
    if DEBUG:
        plt.show()
    else:
        plt.savefig(get_path('./output/plt', uid))
        plt.close()
    # end if

    ##############################

    # https://www.jianshu.com/p/88d663ecdf25
    # 预测(cumsum还原差分)
    st_date = range_date_min + pd.Timedelta(days=2)
    ed_date = range_date_max + pd.Timedelta(days=PREDICT_DAYS)
    forecast = ts_module.predict(st_date, ed_date)
    # 还原一阶
    time_series_restored = (pd.Series().append(forecast).cumsum() + diff_first_fee)
    # 还原二阶
    time_series_restored = (pd.Series().append(time_series_restored).cumsum() + first_fee)

    # 绘图
    plt.plot(pre_data['date'], pre_data['fee'], label='Real')
    time_series_restored.plot(label='Forecast')
    # plt.plot(time_series_restored.index, time_series_restored)
    plt.title('Predict')
    plt.grid()
    plt.legend()
    if DEBUG:
        plt.show()
    else:
        plt.savefig(get_path('./output/plt', str(uid) + '_predict'))
        plt.close()
    # end if

    ##############################

    if DEBUG and index == DEBUG_NUM:
        break
    index += 1
