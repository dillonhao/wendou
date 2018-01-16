import tushare as ts
import pandas as pd
import numpy as np
import datetime

class DataPreparation(object):
    def __init__(self, Instrument, TimeWindow, PerformWindow, ObervationWindow, UpPercent):
        self.__Instrument = Instrument          # Name of the stock
        self.__TimeWindow = TimeWindow                    # int windows for data analysis
        self.__PerformWindow = int(PerformWindow)            # int windows for data analysis
        self.__ObervationWindow = int(ObervationWindow)      # int windows for observation
        self.__UpPercent = UpPercent                    # float percentage, up to which a trend is considered good/bad
        self.__StartTime = (datetime.datetime.now() - datetime.timedelta(days=self.__TimeWindow)).strftime('%Y-%m-%d')
        # __StartTime is max time of entry point
        self.__EndTime = datetime.datetime.now().strftime('%Y-%m-%d')
    # def init_instrument(): #init the instrument data

    
    def init_index(self,index):  #init the index data
        IndexData = ts.get_k_data(index, index=True,start = self.__StartTime,end = self.__EndTime)
        IndexData.set_index('date',inplace = True)
        IndexData.index = pd.DatetimeIndex(IndexData.index)
        return IndexData
    
    # 过去N天点位同比变化（上涨，下跌比率）（三、七、十五天、三十天，六十天，九十天）
    # return percent change from the start to the end
    def PricechangesinlastNdays(self,Inframe,N):
        Series = pd.Series(index = Inframe.iloc[N:-self.__PerformWindow].index)
        idx = Series.index
        for value in idx:
            _Pointer = Inframe.index.get_loc(value.strftime('%Y-%m-%d'))
            _StartTime = _Pointer - N
            Series[value] = (Inframe.iloc[_StartTime].close - Inframe.iloc[_Pointer].close)/Inframe.iloc[_StartTime].close
        return Series

    def PriceshakeinlastNdays(self, Inframe, N):
        # conpare the time, if the max is larger than the min then return the positive number, if not negtive number
        Series = pd.Series(index = Inframe.iloc[N:-self.__PerformWindow].index)
        idx = Series.index
        if indexdf[indexdf.close == indexdf['close'].max()].index > indexdf[
            indexdf.close == indexdf['close'].min()].index:
            return (frame['close'].max() - frame['close'].min()) / frame['close'].min()
        else:
            return -(frame['close'].max() - frame['close'].min()) / frame['close'].max()
    
    # ef data_assemble():                                #assemble all the data
    
    
    def GoodOrBad(self, frame,up):
        if (frame.iloc[0].close - frame.close.max())/frame.iloc[0].close > up and frame.close.min() > frame.iloc[0].close:
            return int(1)
        else:
            return int(0)

dp = DataPreparation('600848',365,30,90,0.2)
tmp=dp.init_index('000001')
print(tmp)