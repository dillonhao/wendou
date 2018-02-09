import pandas as pd
import numpy as np
from math import log


n = 1
m = 5
C = 0.01
lmd = 0.95
timeframe = 600
p = np.matrix('10 0;0 10')
aa = pd.DataFrame(index=tick.index)


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

rls(indexdf.close,ed)