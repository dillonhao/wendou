import pandas as pd
import numpy as np
from math import log
import tushare as ts
import datetime

#define global param
Instrument = '600848'   #define the target instrument
Timeana = 365          #define the length of the time
endtime = datetime.datetime.now().strftime('%Y-%m-%d')
starttime = (datetime.datetime.now() - datetime.timedelta(days = Timeana)).strftime('%Y-%m-%d')

index = '000001'
indexdf = ts.get_k_data('600519',start = starttime,end = endtime)
 #get_k_data is a new interface be careful
indexdf.set_index('date',inplace=True)
indexdf.index = pd.DatetimeIndex(indexdf.index)

def AvgReturn(tick, n, m):
    # defind the x = ln(x1/x2) which is the return of price. return the series data.
    # n is small than m, if not ,convert
    if n > m:
        tmp = n
        n = m
        m = tmp
    x = pd.Series(index=tick.index)
    size = tick.size
    for i, value in enumerate(tick):
        x.iloc[size - i - 1] = log(tick[size - i - n:size - i].mean() / tick[size - i - m:size - i].mean())
    return x


def meb(x, a, b, c):
    # return the membership of PL,PM,PS,AZ,NS,NM,NL
    # x is return , a, b, c is the boundary of the membership
    if x <= a:
        return 0
    if (x > a) and (x <= b):
        return (x-a)/(b-a)
    if (x > b) and (x <= c):
        return (c-x)/(c-b)
    if x > c:
        return 0
    if a == b:
        if x <= b:
            return 1
        if (x > b) and (x <= c):
            return(c-x)/(c-b)
        if x > c:
            return 0
    if b == c:
        if x <= a:
            return 0
        if (x > a) and (x <= b):
            return (x-a)/(b-a);
        if x > b:
            return 1

def ed67(AvgReturn,c):
    # return two pd.Seris one for ed6, another for ed7
    # avgreturn is the return from the avgreturn
    ed6 = pd.Series(index=AvgReturn.index)
    ed7 = pd.Series(index=AvgReturn.index)
    for i,value in enumerate(AvgReturn):
        if np.isnan(value) == False:
            y1 = meb(value, 0, c, 2 * c)
            y2 = meb(value, c, 2 * c, 3 * c)
            y3 = meb(value, 2 * c, 3 * c, 3 * c)
            y4 = meb(value, -2 * c, -c, 0)
            y5 = meb(value, -3 * c, -2 * c, -c)
            y6 = meb(value, -3 * c, -3 * c, -2 * c)
            y7 = meb(value, -c, 0, c)
            ya = y1 + y2 + y3 + y7
            yb = y4 + y5 + y6 + y7
            if ya ==0 :
                ed6.iloc[i]=0
            else:
                ed6.iloc[i] = (0.1 * y1 + 0.2 * y2 + 0.4 * y3) / ya
            if yb == 0:
                ed7.iloc[i]=0
            else:
                ed7.iloc[i] = (0.1 * y4 + 0.2 * y5 + 0.4 * y6) / yb
    return pd.concat([ed6, ed7],axis=1)


n = 1
m = 5
C = 0.01
lmd = 0.95
timeframe = 600
p = np.matrix('10 0;0 10')
#aa = pd.DataFrame(index=tick.index)


def rls(tick):
    # tick is a time series. close is prefer
    MaReturn = AvgReturn(tick, 1, 5)
    ed = ed67(MaReturn, 0.01)
    p = np.matrix('10 0;0 10')
    aa = pd.DataFrame(np.zeros([tick.size + 1, 2]), columns=[1, 2])
    for i, value in enumerate(tick):
        if i < 4:
            continue
        x = np.matrix(ed.iloc[i, :]).T
        aai = np.matrix(aa.iloc[i, :]).T
        K = p * x / (x.T * p * x - 0.95)
        r = log(tick.iloc[i] / tick.iloc[i - 1])
        aa.iloc[i + 1] = (aai + K * (r - x.T * aai)).T
        p = (p - K * x.T * p) / 0.95
        # P=(P-K*x'*P)/lmd
        # print "/n", x
        # print "/n", aai
        # print "/n", K,
        # print "/n", r,
        # print "/n", p
    return aa

out = rls(indexdf.close)

