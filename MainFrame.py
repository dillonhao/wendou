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

    def VolumnsuminlastNdays(self, Inframe, N):
        # accumulated volumns in last N days
        Series = pd.Series(index = Inframe.iloc[N:-self.__PerformWindow].index)
        idx = Series.index
        for value in idx:
            _Pointer = Inframe.index.get_loc(value.strftime('%Y-%m-%d'))
            _StartTime = _Pointer - N
            df = Inframe.iloc[_StartTime: _Pointer]
            Series[value] = df['close'].sum()
        return Series

    def IndexSTDinlastNdays(self, Inframe, N):
        #std of the index
        Series = pd.Series(index = Inframe.iloc[N:-self.__PerformWindow].index)
        idx = Series.index
        for value in idx:
            _Pointer = Inframe.index.get_loc(value.strftime('%Y-%m-%d'))
            _StartTime = _Pointer - N
            df = Inframe.iloc[_StartTime: _Pointer]
            Series[value] = df['close'].std()
        return Series

    def IndexPercentageSTDinlastNdays(self, Inframe, N):
        #std of the percent change
        Series = pd.Series(index = Inframe.iloc[N:-self.__PerformWindow].index)
        idx = Series.index
        for value in idx:
            _Pointer = Inframe.index.get_loc(value.strftime('%Y-%m-%d'))
            _StartTime = _Pointer - N
            df = Inframe.iloc[_StartTime: _Pointer]
            ChangePercentage = (df.close - df.close.shift(1)) / df.close
            ChangePercentage.dropna(inplace=True)
            Series[value] = ChangePercentage.std()
        return Series

    def MaxContinuousUpDownInLastNdays(self, Inframe, N):
        #Not designed to work alone, will call MaxLenofUpDownsinlastNdays to get the data.
        df = pd.DataFrame(index = Inframe.iloc[N:-self.__PerformWindow].index, columns=['UpDur','DownDur','UpPrice','DownPrice'])
        idx = df.index
        for value in idx:
            _Pointer = Inframe.index.get_loc(value.strftime('%Y-%m-%d'))
            _StartTime = _Pointer - N
            UpDownPrice = self.MaxLenofUpDownsinlastNdays(Inframe, _StartTime, _Pointer)
            df.loc[value].UpDur = UpDownPrice.loc[True,'Duration']
            df.loc[value].DownDur =UpDownPrice.loc[False,'Duration']
            df.loc[value].UpPrice = UpDownPrice.loc[True,'PriceChange']
            df.loc[value].DownPrice = UpDownPrice.loc[False,'PriceChange']
        return df

    def MaxLenofUpDownsinlastNdays(self,Inframe, _start, _End):
        # cal the max continuous up and down in the timeseries and return the up percentage and down percentage
        '''
        return  example
                Start 	End 	Duration 	PriceChange
        True 	0 	8 	9 	0.042164
        False 	0 	0 	0 	0.000000
        true stands for up, false stands for down
        return the nestest and longest time of up and down
        '''
        # prepare the data for logic sequence
        UpDowns = Inframe.iloc[_start:_End]
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
                        point,
                        point + Length[value] - 1)  # when maxlength is updated the start and end point is also updated
                else:
                    pass
            else:
                Length[:] = int(
                    1)  # if not match then min length for up and down is both one, there are always up and downs in a bool series
                point = index

        if MaxLength[True] != 0:
            UpStart = StartEnd.loc[True, 'Start']
            UpEnd = StartEnd.loc[True, 'End']
            UpPrice = (Inframe.iloc[UpEnd].close - Inframe.iloc[UpStart].close) / Inframe.iloc[UpStart].close
        else:  # when the length is 0, the price is down all the time so the UpPrice is zero
            UpPrice = 0
        if MaxLength[False] != 0:
            DownStart = StartEnd.loc[False, 'Start']
            downEnd = StartEnd.loc[False, 'End']
            DownPrice = (Inframe.iloc[downEnd].close - Inframe.iloc[DownStart].close) / Inframe.iloc[DownStart].close
        else:
            DownPrice = 0

        PriceChange = pd.Series([UpPrice, DownPrice], index=[True, False])

        StartEnd['Duration'] = MaxLength  # connect duration and the start and end time
        StartEnd['PriceChange'] = PriceChange
        return StartEnd


dp = DataPreparation('600848',365,30,90,0.2)
tmp=dp.init_index('000001')
tmp1 = dp.MaxContinuousUpDownInLastNdays(tmp,30)
