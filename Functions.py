import tushare as ts
import pandas as pd
import numpy as np
import datetime
import time

# define global param
Instrument = '600848'  # define the target instrument
Timeana = 365  # define the length of the time
endtime = datetime.datetime.now().strftime('%Y-%m-%d')
starttime = (datetime.datetime.now() - datetime.timedelta(days=Timeana)).strftime('%Y-%m-%d')

index = '000001'
indexdf = ts.get_k_data('000001', index=True, start=starttime, end=endtime)
# get_k_data is a new interface be careful
indexdf.set_index('date', inplace=True)
indexdf.index = pd.DatetimeIndex(indexdf.index)
# Date in the returned dataframe is a string. we convert it into a datatimeindex index

#############################################################
# 过去N天高开、低开次数（三、七、十五天、三十天，六十天，九十天）

def LowopeninlastNdays(frame, N):
    df = frame.tail(N)
    to_opens = df['open'].shift(1)
    ye_closes = df['close']
    offset = to_opens - ye_closes
    return len(offset[offset < 0])  # 返回所有offset序列中小于0的数量


# cal the number of lower open in last N days in the index
# today's open - yesterday's close

def HigheopeninlastNdays(frame, N):
    df = frame.tail(N)
    to_opens = df['open'].shift(1)
    ye_closes = df['close']
    offset = to_opens - ye_closes
    return len(offset[offset > 0])  # 返回所有offset序列中小于0的数量

# cal the number of higher open in last N days in the index
# today's open - yesterday's close
# 【注意】：可能有个bug，shift（1）后第一个数是NAN，减去一个实数还是NAN
#############################################################
# 过去N天上涨、下跌次数（三、七、十五天、三十天，六十天，九十天）

def UpinlastNdays(frame, N):
    df_1 = frame.tail(N)
    df = df_1['close'] - df_1['open']
    return len(df[df > 0])


def DowninlastNdays(frame, N):
    df_1 = frame.tail(N)
    df = df_1['close'] - df_1['open']
    return len(df[df < 0])


#############################################################
# 过去N天最长连续上涨，下跌时间，和价格变化（三、七、十五天、三十天，六十天，九十天）
# 注意：从这个版本的函数开始，输入变成了indexdf.tail(N)，注意这个变化。
# cal the max up and down in the timeseries and return the up percentage and down percentage
'''
return  example
        Start 	End 	Duration 	PriceChange
True 	0 	8 	9 	0.042164
False 	0 	0 	0 	0.000000
true stands for up, false stands for down
return the nestest and longest time of up and down
'''


def MaxlenofupdownsinlastNdays(frame):
    # prepare the data for logic sequence
    UpDowns = frame
    UpDowns = UpDowns['close'].shift(1) - UpDowns['close']
    UpDowns.dropna(inplace=True)  # drop the top NaN value. the NaN is neither >0 or < 0
    UpDowns = (UpDowns < 0)  # convert the price change into true or false sequences
    # initial the variables
    MaxLength = pd.Series([0, 0], index=[True, False], dtype=int)  # record the max length in a series
    Length = pd.Series([0, 0], index=[True, False], dtype=int)  # temp variable and compare with the maxlength
    StartEnd = pd.DataFrame(np.zeros((2, 2)), index=[True, False], columns=['Start', 'End'],
                            dtype=int)  # record the start and end point of the up and downs
    Length[:] = int(0)  # by default the length is zero, in case of no up or down in a series
    point = int(0)  # point to the start of a trend, and update to the index in case of a change in the trend

    for index, value in enumerate(UpDowns):
        if value == UpDowns.iat[point]:
            Length[value] = Length[value] + 1  # if the value match the start of the trend length++
            if MaxLength[value] <= Length[
                value]:  # if the length is large then the previous maxlength then update the maxlength
                MaxLength[value] = Length[value]
                StartEnd.loc[value] = (
                point, point + Length[value] - 1)  # when maxlength is updated the start and end point is also updated
            else:
                pass
        else:
            Length[:] = int(
                1)  # if not match then min length for up and down is both one, there are always up and downs in a bool series
            point = index

    if MaxLength[True] != 0:
        UpStart = StartEnd.loc[True, 'Start']
        UpEnd = StartEnd.loc[True, 'End']
        UpPrice = (frame.iloc[UpEnd].close - frame.iloc[UpStart].close) / frame.iloc[UpStart].close
    else:  # when the length is 0, the price is down all the time so the UpPrice is zero
        UpPrice = 0
    if MaxLength[False] != 0:
        DownStart = StartEnd.loc[False, 'Start']
        downEnd = StartEnd.loc[False, 'End']
        DownPrice = (frame.iloc[downEnd].close - frame.iloc[DownStart].close) / frame.iloc[DownStart].close
    else:
        DownPrice = 0

    PriceChange = pd.Series([UpPrice, DownPrice], index=[True, False])

    StartEnd['Duration'] = MaxLength  # connect duration and the start and end time
    StartEnd['PriceChange'] = PriceChange
    return StartEnd



##############################################################
[class ready]
#过去N天点位同比变化（上涨，下跌比率）（三、七、十五天、三十天，六十天，九十天）
#return percent change from the start to the end
def PricechangesinlastNdays(frame):
    return (frame.iloc[-1].close - frame.iloc[0].close)/frame.iloc[-1].close

#################################################################
#过去N天最高点位和最低点位的震动比例（三、七、十五天、三十天，六十天，九十天）
#return the max to min percentage change, if go up return positive number, if go down return negtive number
def PriceshakeinlastNdays(frame):
    #conpare the time, if the max is larger than the min then return the positive number, if not negtive number
    if indexdf[indexdf.close == indexdf['close'].max()].index > indexdf[indexdf.close == indexdf['close'].min()].index:
        return (frame['close'].max() - frame['close'].min())/frame['close'].min()
    else:
        return -(frame['close'].max() - frame['close'].min())/frame['close'].max()


##################################################################
#过去N天成交量累计（三、七、十五天、三十天，六十天，九十天）
def VolumnsuminlastNdays(frame):
    return frame.volume.sum()

###################################################################
#过去N天指数绝对值的标准差
def IndexSTDinlastNdays(frame):
    return frame.close.std()


#####################################################################
#过去N天指数波动率的标准差
def IndexpercentageSTDinlastNdays(frame):
    ChangePercentage = (frame.close-frame.close.shift(1))/frame.close
    ChangePercentage.dropna(inplace=True)
    return ChangePercentage.std()
