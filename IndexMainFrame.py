import tushare as ts
import pandas as pd
import numpy as np
import datetime


class IndexMainframe(object):
    def __init__(self, index, timewindow, performwindow, obervationwindow, uppercent):
        #self.__instrument = instrument  # Name of the stock
        self.__timewindow = timewindow  # int windows for data analysis
        self.__performwindow = int(performwindow)  # int windows for data analysis
        self.__obervationwindow = int(obervationwindow)  # int windows for observation
        self.__uppercent = uppercent  # float percentage, up to which a trend is considered good/bad
        self.__starttime = (datetime.datetime.now() - datetime.timedelta(days=self.__timewindow)).strftime('%Y-%m-%d')
        # __starttime is max time of entry point
        self.__endtime = datetime.datetime.now().strftime('%Y-%m-%d')
        IndexData = ts.get_k_data(index, index=True, start=self.__starttime, end=self.__endtime)
        IndexData.set_index('date', inplace=True)
        IndexData.index = pd.DatetimeIndex(IndexData.index)
        self.__indexdata = IndexData

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
            if inframe[inframe.close == inframe['close'].max()].index > inframe[
                inframe.close == inframe['close'].min()].index:
                Series[value] = (inframe.iloc[_starttime:_pointer].close.max() - inframe.iloc[
                                                                                 _starttime:_pointer].close.min()) / inframe.iloc[
                                                                                                                     _starttime:_pointer].close.min()
            else:
                Series[value] = (inframe.iloc[_starttime:_pointer].close.max() - inframe.iloc[
                                                                                 _starttime:_pointer].close.min()) / inframe.iloc[
                                                                                                                     _starttime:_pointer].close.max()
        return Series

    def GoodOrBad(self, frame, up):
        if (frame.iloc[0].close - frame.close.max()) / frame.iloc[0].close > up and frame.close.min() > frame.iloc[
            0].close:
            return int(1)
        else:
            return int(0)

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

    def IndexSTDinlastNdays(self, inframe, N):
        # std of the index
        Series = pd.Series(index=inframe.iloc[N:-self.__performwindow].index)
        idx = Series.index
        for value in idx:
            _pointer = inframe.index.get_loc(value.strftime('%Y-%m-%d'))
            _starttime = _pointer - N
            df = inframe.iloc[_starttime: _pointer]
            Series[value] = df['close'].std()
        return Series

    def IndexPercentageSTDinlastNdays(self, inframe, N):
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
                          columns=['UpDur', 'DownDur', 'UpPrice', 'DownPrice'])
        idx = df.index
        for value in idx:
            _pointer = inframe.index.get_loc(value.strftime('%Y-%m-%d'))
            _starttime = _pointer - N
            UpDownPrice = self.MaxLenofUpDownsinlastNdays(inframe, _starttime, _pointer)
            df.loc[value].UpDur = UpDownPrice.loc[True, 'Duration']
            df.loc[value].DownDur = UpDownPrice.loc[False, 'Duration']
            df.loc[value].UpPrice = UpDownPrice.loc[True, 'PriceChange']
            df.loc[value].DownPrice = UpDownPrice.loc[False, 'PriceChange']
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
        print('im in here.hahah')
        indexDataFrame = pd.DataFrame(index = self.__indexdata.index)
        for value in enumerate(datelist):
            indexDataFrame['PriceChangesinlastNdays' + str(value)] = self.PriceChangesinlastNdays(self.__indexdata, value)
            indexDataFrame['PriceShakeinlastNdays' + str(value)] = self.PriceShakeinlastNdays(self.__indexdata, value)
            indexDataFrame['LowOpeninlastNdays' + str(value)] = self.LowOpeninlastNdays(self.__indexdata, value)
            indexDataFrame['UpinlastNdays' + str(value)] = self.UpinlastNdays(self.__indexdata, value)
            indexDataFrame['InDayShakeinlastNdays' + str(value)] = self.InDayShakeinlastNdays(self.__indexdata, value)
            indexDataFrame['VolumnsuminlastNdays' + str(value)] = self.VolumnsuminlastNdays(self.__indexdata, value)
            indexDataFrame['IndexSTDinlastNdays' + str(value)] = self.IndexSTDinlastNdays(self.__indexdata, value)
            indexDataFrame['IndexPercentageSTDinlastNdays' + str(value)] = self.IndexPercentageSTDinlastNdays(self.__indexdata, value)
            indexDataFrame['MaxContinuousUpDownInLastNdays' + str(value)] = self.MaxContinuousUpDownInLastNdays(self.__indexdata, value)
        return indexDataFrame


alist = [30,60]
Myclass = IndexMainframe('000001', 365, 30, 90, 0.2)
#tmp = dp.init_index('000001')
test = Myclass.data_assemble(alist)
