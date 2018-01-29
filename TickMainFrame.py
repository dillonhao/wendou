import tushare as ts
import pandas as pd
import numpy as np
import datetime


class TickMainFrame(object):
    def __init__(self, tick, timewindow, performwindow, obervationwindow, uppercent):
        #self.__instrument = instrument  # Name of the stock
        self.__timewindow = timewindow  # int windows for data analysis
        self.__performwindow = int(performwindow)  # int windows for data analysis
        self.__obervationwindow = int(obervationwindow)  # int windows for observation
        self.__uppercent = uppercent  # float percentage, up to which a trend is considered good/bad
        self.__starttime = (datetime.datetime.now() - datetime.timedelta(days=self.__timewindow)).strftime('%Y-%m-%d')
        # __starttime is max time of entry point
        self.__endtime = datetime.datetime.now().strftime('%Y-%m-%d')
        TickData = ts.get_k_data(tick, start=self.__starttime, end=self.__endtime)
        TickData.set_index('date', inplace=True)
        TickData.index = pd.DatetimeIndex(TickData.index)
        self.__Tickdata = TickData

    # return percent change from the start to the end
    def PriceChangesinlastNdays(self, inframe, N):
        Series = pd.Series(index=inframe.iloc[N:-self.__performwindow].index)
        idx = Series.index
        for value in idx:
            _pointer = inframe.index.get_loc(value.strftime('%Y-%m-%d'))
            _starttime = _pointer - N
            Series[value] = (inframe.iloc[_starttime].close - inframe.iloc[_pointer].close) / inframe.iloc[
                _starttime].close
        return Series

    def PriceShakeinlastNdays(self, inframe, N):
        # return the max to min percentage change, if go up return positive number, if go down return negtive number
        # conpare the time, if the max is larger than the min then return the positive number, if not negtive number
        Series = pd.Series(index=inframe.iloc[N:-self.__performwindow].index)
        idx = Series.index
        for value in idx:
            _pointer = inframe.index.get_loc(value.strftime('%Y-%m-%d'))
            _starttime = _pointer - N
            #if inframe[inframe.close == inframe['close'].max()].index > inframe[
                #inframe.close == inframe['close'].min()].index:
            if inframe.iloc[_starttime:_pointer].close.idxmax() > inframe.iloc[_starttime:_pointer].close.idxmin():
                Series[value] = (inframe.iloc[_starttime:_pointer].close.max() - inframe.iloc[
                                                                                 _starttime:_pointer].close.min()) / inframe.iloc[
                                                                                                                     _starttime:_pointer].close.min()
            else:
                Series[value] = (inframe.iloc[_starttime:_pointer].close.min() - inframe.iloc[
                                                                                 _starttime:_pointer].close.max()) / inframe.iloc[
                                                                                                                     _starttime:_pointer].close.max()
        return Series

    def GoodOrBad(self, inframe, up):
        #define good or bad
        Series = pd.Series(index=inframe.iloc[0:-self.__performwindow].index,name='KGB')
        idx = Series.index
        for value in idx:
            _pointer = inframe.index.get_loc(value.strftime('%Y-%m-%d'))
            _endtime = _pointer + self.__performwindow
            if (inframe.iloc[_pointer:_endtime].close.max() - inframe.iloc[_pointer].close) / inframe.iloc[_pointer].close > up and inframe.iloc[_pointer:_endtime].close.min() < inframe.iloc[_pointer].close:
                Series[value] = int(1)
            else:
                Series[value] = int(0)
        return Series

    def LowOpeninlastNdays(self, inframe, N):
        # Higher or Lower open is last N days
        Series = pd.Series(index=inframe.iloc[N:-self.__performwindow].index)
        idx = Series.index
        for value in idx:
            _pointer = inframe.index.get_loc(value.strftime('%Y-%m-%d'))
            _starttime = _pointer - N
            to_opens = inframe.iloc[_starttime:_pointer].open.shift(1)
            ye_closes = inframe.iloc[_starttime:_pointer].open
            offset = to_opens - ye_closes
            Series[value] = len(offset[offset < 0])
        return Series

    def UpinlastNdays(self, inframe, N):
        # cal the up days in the last N days
        Series = pd.Series(index=inframe.iloc[N:-self.__performwindow].index)
        idx = Series.index
        for value in idx:
            _pointer = inframe.index.get_loc(value.strftime('%Y-%m-%d'))
            _starttime = _pointer - N
            df_1 = inframe.iloc[_starttime:_pointer]
            df = df_1['close'] - df_1['open']
            Series[value] = len(df[df > 0])
        return Series

    def InDayShakeinlastNdays(self, inframe, N):
        # cal the percentage shake std within days
        Series = pd.Series(index=inframe.iloc[N:-self.__performwindow].index)
        idx = Series.index
        for value in idx:
            _pointer = inframe.index.get_loc(value.strftime('%Y-%m-%d'))
            _starttime = _pointer - N
            df_1 = inframe.iloc[_starttime:_pointer]
            df = (df_1['close'] - df_1['open']) * 100 / df_1['open']
            Series[value] = df.std()
        return Series

    def VolumnsuminlastNdays(self, inframe, N):
        # accumulated volumns in last N days
        Series = pd.Series(index=inframe.iloc[N:-self.__performwindow].index)
        idx = Series.index
        for value in idx:
            _pointer = inframe.index.get_loc(value.strftime('%Y-%m-%d'))
            _starttime = _pointer - N
            df = inframe.iloc[_starttime: _pointer]
            Series[value] = df['close'].sum()
        return Series

    def TickSTDinlastNdays(self, inframe, N):
        # std of the Tick
        Series = pd.Series(index=inframe.iloc[N:-self.__performwindow].index)
        idx = Series.index
        for value in idx:
            _pointer = inframe.index.get_loc(value.strftime('%Y-%m-%d'))
            _starttime = _pointer - N
            df = inframe.iloc[_starttime: _pointer]
            Series[value] = df['close'].std()
        return Series

    def TickPercentageSTDinlastNdays(self, inframe, N):
        # std of the percent change
        Series = pd.Series(index=inframe.iloc[N:-self.__performwindow].index)
        idx = Series.index
        for value in idx:
            _pointer = inframe.index.get_loc(value.strftime('%Y-%m-%d'))
            _starttime = _pointer - N
            df = inframe.iloc[_starttime: _pointer]
            ChangePercentage = (df.close - df.close.shift(1)) / df.close
            ChangePercentage.dropna(inplace=True)
            Series[value] = ChangePercentage.std()
        return Series

    def MaxContinuousUpDownInLastNdays(self, inframe, N):
        # Not designed to work alone, will call MaxLenofUpDownsinlastNdays to get the data.
        df = pd.DataFrame(index=inframe.iloc[N:-self.__performwindow].index,
                          columns=['TickUpDur', 'TickDownDur', 'TickUpPrice', 'TickDownPrice'])
        idx = df.index
        for value in idx:
            _pointer = inframe.index.get_loc(value.strftime('%Y-%m-%d'))
            _starttime = _pointer - N
            UpDownPrice = self.MaxLenofUpDownsinlastNdays(inframe, _starttime, _pointer)
            df.loc[value].TickUpDur = UpDownPrice.loc[True, 'Duration']
            df.loc[value].TickDownDur = UpDownPrice.loc[False, 'Duration']
            df.loc[value].TickUpPrice = UpDownPrice.loc[True, 'PriceChange']
            df.loc[value].TickDownPrice = UpDownPrice.loc[False, 'PriceChange']
        return df

    def MaxLenofUpDownsinlastNdays(self, inframe, _start, _End):
        # Not design to work alone. cal the max continuous up and down in the timeseries and return the up percentage and down percentage
        '''
        return  example
                Start 	End 	Duration 	PriceChange
        True 	0 	8 	9 	0.042164
        False 	0 	0 	0 	0.000000
        true stands for up, false stands for down
        return the nestest and longest time of up and down
        '''
        # prepare the data for logic sequence
        UpDowns = inframe.iloc[_start:_End]
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
            UpPrice = (inframe.iloc[UpEnd].close - inframe.iloc[UpStart].close) / inframe.iloc[UpStart].close
        else:  # when the length is 0, the price is down all the time so the UpPrice is zero
            UpPrice = 0
        if MaxLength[False] != 0:
            DownStart = StartEnd.loc[False, 'Start']
            downEnd = StartEnd.loc[False, 'End']
            DownPrice = (inframe.iloc[downEnd].close - inframe.iloc[DownStart].close) / inframe.iloc[DownStart].close
        else:
            DownPrice = 0

        PriceChange = pd.Series([UpPrice, DownPrice], index=[True, False])

        StartEnd['Duration'] = MaxLength  # connect duration and the start and end time
        StartEnd['PriceChange'] = PriceChange
        return StartEnd

    def data_assemble(self, datelist):
        # assemble all the data
        TickDataFrame = pd.DataFrame(index=self.__Tickdata.index)
        s0 = pd.Series(self.GoodOrBad(self.__Tickdata, self.__uppercent), name='Tick_KGB')
        for value in datelist:
            # s0 = pd.Series(self.GoodOrBad(self.__Tickdata, self.__uppercent), name='Tick_KGB')
            s1 = pd.Series(self.PriceChangesinlastNdays(self.__Tickdata, value),
                           name='TickPriceChangesinlastNdays' + str(value))
            s2 = pd.Series(self.PriceShakeinlastNdays(self.__Tickdata, value),
                           name='TickPriceShakeinlastNdays' + str(value))
            s3 = pd.Series(self.LowOpeninlastNdays(self.__Tickdata, value), name='TickLowOpeninlastNdays' + str(value))
            s4 = pd.Series(self.UpinlastNdays(self.__Tickdata, value), name='TickUpinlastNdays' + str(value))
            s5 = pd.Series(self.InDayShakeinlastNdays(self.__Tickdata, value),
                           name='TickInDayShakeinlastNdays' + str(value))
            s6 = pd.Series(self.VolumnsuminlastNdays(self.__Tickdata, value), name='TickVolumnsuminlastNdays' + str(value))
            s7 = pd.Series(self.TickSTDinlastNdays(self.__Tickdata, value), name='TickSTDinlastNdays' + str(value))
            s8 = pd.Series(self.TickPercentageSTDinlastNdays(self.__Tickdata, value),
                           name='TickPercentageSTDinlastNdays' + str(value))
            s9 = pd.DataFrame(self.MaxContinuousUpDownInLastNdays(self.__Tickdata, value))
            df = pd.concat([s1, s2, s3, s4, s5, s6, s7, s8,s9], axis=1)
            TickDataFrame = pd.concat([TickDataFrame, df], axis=1)
        TickDataFrame = pd.concat([TickDataFrame, s0], axis=1)
        print('haha, Im here')
        return TickDataFrame

'''
alist = [5, 10, 30, 60, 90]
Myclass = TickMainframe('600519', 730, 30, 90, 0.1)
# tmp = dp.init_Tick('000001')
test = Myclass.data_assemble(alist)
# test = Myclass.GoodOrBad(Tickdf,0.1)
'''