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
    
    # return percent change from the start to the end
    def PriceChangesinlastNdays(self,Inframe,N):
        Series = pd.Series(index = Inframe.iloc[N:-self.__PerformWindow].index)
        idx = Series.index
        for value in idx:
            _Pointer = Inframe.index.get_loc(value.strftime('%Y-%m-%d'))
            _StartTime = _Pointer - N
            Series[value] = (Inframe.iloc[_StartTime].close - Inframe.iloc[_Pointer].close)/Inframe.iloc[_StartTime].close
        return Series

    def PriceShakeinlastNdays(self, Inframe, N):
        # return the max to min percentage change, if go up return positive number, if go down return negtive number
        # conpare the time, if the max is larger than the min then return the positive number, if not negtive number
        Series = pd.Series(index = Inframe.iloc[N:-self.__PerformWindow].index)
        idx = Series.index
        for value in idx:
            _Pointer = Inframe.index.get_loc(value.strftime('%Y-%m-%d'))
            _StartTime = _Pointer - N
            if Inframe[Inframe.close == Inframe['close'].max()].index > Inframe[Inframe.close == Inframe['close'].min()].index:
                Series[value] =  (Inframe.iloc[_StartTime:_Pointer].close.max() - Inframe.iloc[_StartTime:_Pointer].close.min()) / Inframe.iloc[_StartTime:_Pointer].close.min()
            else:
                Series[value] = (Inframe.iloc[_StartTime:_Pointer].close.max() - Inframe.iloc[_StartTime:_Pointer].close.min()) / Inframe.iloc[_StartTime:_Pointer].close.max()
        return Series
    # def data_assemble():                                #assemble all the data
    
    
    def GoodOrBad(self, frame,up):
        if (frame.iloc[0].close - frame.close.max())/frame.iloc[0].close > up and frame.close.min() > frame.iloc[0].close:
            return int(1)
        else:
            return int(0)

    def LowOpeninlastNdays(self, Inframe, N):
        # Higher or Lower open is last N days
        Series = pd.Series(index = Inframe.iloc[N:-self.__PerformWindow].index)
        idx = Series.index
        for value in idx:
            _Pointer = Inframe.index.get_loc(value.strftime('%Y-%m-%d'))
            _StartTime = _Pointer - N
            to_opens = Inframe.iloc[_StartTime:_Pointer].open.shift(1)
            ye_closes = Inframe.iloc[_StartTime:_Pointer].open
            offset = to_opens - ye_closes
            Series[value] = len(offset[offset < 0])
        return Series

    def UpinlastNdays(self, Inframe, N):
        # cal the up days in the last N days
        Series = pd.Series(index = Inframe.iloc[N:-self.__PerformWindow].index)
        idx = Series.index
        for value in idx:
            _Pointer = Inframe.index.get_loc(value.strftime('%Y-%m-%d'))
            _StartTime = _Pointer - N
            df_1 = Inframe.iloc[_StartTime:_Pointer]
            df = df_1['close'] - df_1['open']
            Series[value] = len(df[df > 0])
        return Series

    def InDayShakeinlastNdays(self, Inframe, N):
        # cal the percentage shake std within days
        Series = pd.Series(index = Inframe.iloc[N:-self.__PerformWindow].index)
        idx = Series.index
        for value in idx:
            _Pointer = Inframe.index.get_loc(value.strftime('%Y-%m-%d'))
            _StartTime = _Pointer - N
            df_1 = Inframe.iloc[_StartTime:_Pointer]
            df = (df_1['close'] - df_1['open'])*100/df_1['open']
            Series[value] = df.std()
        return Series

dp = DataPreparation('600848',365,30,90,0.2)
tmp=dp.init_index('000001')
tmp1 = dp.InDayShakeinlastNdays(tmp,30)