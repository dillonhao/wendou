import numpy as np
import pandas as pd
from math import log
#import os

def meb(x, a, b, c):
    # return the membership of PL,PM,PS,AZ,NS,NM,NL
    # x is return , a, b, c is the boundary of the membership
    if x <= a:
        return 0.0
    if (x > a) and (x <= b):
        return (x-a)/(b-a)
    if (x > b) and (x <= c):
        return (c-x)/(c-b)
    if x > c:
        return 0.0
    if a == b:
        if x <= b:
            return 1.0
        if (x > b) and (x <= c):
            return(c-x)/(c-b)
        if x > c:
            return 0.0
    if b == c:
        if x <= a:
            return 0.0
        if (x > a) and (x <= b):
            return (x-a)/(b-a)
        if x > b:
            return 1.0

def init(context):
    logger.info("init")
    context.s1 = "002032.XSHE"
    #if instruments(context.s1).days_from_listed(date=None)<366:
        #os._exit()
    update_universe(context.s1)
    # 是否已发送了order
    context.fired = False
    context.P = np.matrix('10 0;0 10')
    context.c=0.01
    context.lmd=0.9
    context.aa = pd.DataFrame(np.zeros([1, 2]), columns=[0, 1])
    #print(aa)
    #context.c = 0.01

def before_trading(context):
    c=context.c
    lmd=context.lmd
    P = context.P
    aa = context.aa.tail(1)
    aai = np.matrix(aa).T
    try:
        numerator = history_bars(context.s1, 1, '1d', 'close').mean()
        denominator = history_bars(context.s1, 5, '1d', 'close').mean()
        tmp = history_bars(context.s1, 2, '1d', 'close')
        r  = log(tmp[1]/tmp[0])
        avg_return = log(numerator/denominator)
        y1 = meb(avg_return, 0, c, 2 * c)
        y2 = meb(avg_return, c, 2 * c, 3 * c)
        y3 = meb(avg_return, 2 * c, 3 * c, 3 * c)
        y4 = meb(avg_return, -2 * c, -c, 0)
        y5 = meb(avg_return, -3 * c, -2 * c, -c)
        y6 = meb(avg_return, -3 * c, -3 * c, -2 * c)
        y7 = meb(avg_return, -c, 0, c)
        ya = y1 + y2 + y3 + y7
        yb = y4 + y5 + y6 + y7
        #print(ya,yb)
        if ya==0:
            ed6=0
        else:
            ed6 = (0.1 * y1 + 0.2 * y2 + 0.4 * y3) / ya
        if yb==0:
            ed7=0
        else:
            ed7 = (0.1 * y4 + 0.2 * y5 + 0.4 * y6) / yb
        #print(ed6,ed7)
        X = np.matrix([[ed6],[ed7]])
        K = P * X / (X.T * P * X - lmd)
        aat = (aai + K * (r - X.T * aai)).T
        context.P = (P - K * X.T * P) / lmd
        #print(context.aa.append(pd.DataFrame(aat), ignore_index=True))
        context.aa=context.aa.append(pd.DataFrame(aat), ignore_index=True) 
    except:
        print("Error when trying")
        #print(tmp)
    
def handle_bar(context, bar_dict):

    # 开始编写你的主要的算法逻辑

    # bar_dict[order_book_id] 可以拿到某个证券的bar信息
    # context.portfolio 可以拿到现在的投资组合状态信息

    # 使用order_shares(id_or_ins, amount)方法进行落单
    # TODO: 开始编写你的算法吧！
    aa = context.aa.tail(1)
    print("im running")
    if aa.iloc[0,0]>0:
        # order_percent并且传入1代表买入该股票并且使其占有投资组合的100%
        order_percent(context.s1, 0.2)
        #context.fired = True
    else:
        order_percent(context.s1, -0.5)