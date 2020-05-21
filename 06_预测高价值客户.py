import numpy as np
import pandas as pd
import statsmodels
import matplotlib.pyplot as plt

# 读取数据
ids = pd.read_csv("./output/ids.csv")['id']
df = pd.read_csv("./output/time_sequence.csv", parse_dates=['date'])
di = pd.DatetimeIndex(df['date'])


