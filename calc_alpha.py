"""
本函数由于计算A股各股票的alpha以及beta系数用于评估其系统性风险和个股风险的收益率
"""

import pandas as pd
import numpy as np
from math import *
import matplotlib.pyplot as plt

# 读取csv数据转换成dataframe格式

def close_sheet(stockname, startdate="2015-01-01", enddate=pd.datetime.now()):
    # 格式为stokname(list), startdate, enddate(2020-9-9)
    # 输出结果为空表
    dateindex = pd.date_range(startdate, enddate)
    stock_close = pd.DataFrame(index=dateindex, columns=stockname)
    return stock_close

def read_stock_close(nan_sheet, stockname, closename):
    # 格式为stokname(list), closename用于指定收盘价的列名，格式为str
    # 由于我们将用收盘价计算收益率，波动率等指标，暂时先将其单独拿出来做一个dataframe
    for i in len(stockname):
        # 逐个录入
        i_data = pd.read_csv(stockname[i] + ".csv")
        nan_sheet[stockname[i]] = i_data[closename]
    return nan_sheet

def stat(datain):
    close_mean = datain.mean()
    close_volatility = np.sqrt(datain.var())
    close_covariance = datain.cov()
    # close_describe = datain.describe()
    return close_mean, close_volatility, close_covariance

from scipy.optimize import minimize

def marketportfolio(datain, stockmean, stockcov):
    # 利用efficient frontier 寻找 tangency portfolio
    # datain 为各股历史数据，index为时间序列，column为股票代码, dim=m*n
    # stockmean, stockvolatility, dim=1*n
    # stockcov , dim=n*n
    m, n = datain.shape
    for ret in np.arange(0, 0.02, 0.0001):
        fun = lambda x : np.sqrt(np.dot(x, np.dot(stockcov, x.T)))
        cons = ({'type': 'eq', 'fun': lambda x: np.dot(x, stockmean) - ret},
                {'type': 'eq', 'fun': lambda x: sum(x) - 1})
        x0 = np.zeros(n)
        x0[0] = 1
        res = minimiza(fun, x0, method='SLSQP', constraints=cons)
    

