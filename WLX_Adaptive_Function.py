import pandas as pd
import numpy as np
from math import log


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
            return 1;