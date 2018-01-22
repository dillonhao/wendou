import tushare as ts
import pandas as pd
import numpy as np
import datetime
import talib as ta


class TaMainFrame(object):
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

    def ADX(self):
        adx = ta.ADX(self.__Tickdata['high'].values, self.__Tickdata['low'].values, self.__Tickdata['close'].values, timeperiod=14)
        return pd.Series(adx, index=self.__Tickdata.index)

    def ADXR(self):
        adxr = ta.ADXR(self.__Tickdata['high'].values, self.__Tickdata['low'].values, self.__Tickdata['close'].values, timeperiod=14)
        return pd.Series(adxr, index=self.__Tickdata.index)

    def AROON(self):
        aroon = ta.AROON(self.__Tickdata['high'].values, self.__Tickdata['low'].values, timeperiod=14)
        aroondf = {'aroonup': aroon[0], 'aroondown': aroon[1]}
        return pd.DataFrame(aroondf,index=self.__Tickdata.index)

    def AROONOSC(self):
        arroonosc = ta.AROONOSC(self.__Tickdata['high'].values, self.__Tickdata['low'].values, timeperiod=14)
        return pd.Series(arroonosc, index=self.__Tickdata.index)

    def BOP(self):
        bop = ta.BOP(self.__Tickdata['open'].values,self.__Tickdata['high'].values, self.__Tickdata['low'].values, self.__Tickdata['close'].values)
        return pd.Series(bop, index=self.__Tickdata.index)

    def CCI(self):
        cci = ta.CCI(self.__Tickdata['high'].values, self.__Tickdata['low'].values, self.__Tickdata['close'].values, timeperiod=14)
        return pd.Series(cci, index=self.__Tickdata.index)

    def CMO(self):
        cmo = ta.CMO(self.__Tickdata['close'].values, timeperiod=14)
        return pd.Series(cmo, index=self.__Tickdata.index)

    def DX(self):
        dx = ta.DX(self.__Tickdata['high'].values, self.__Tickdata['low'].values, self.__Tickdata['close'].values, timeperiod=14)
        return pd.Series(dx, index=self.__Tickdata.index)

    def MACD(self):
        #macd, macdsignal, macdhist = MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
        macd = ta.MACD(self.__Tickdata['close'].values,fastperiod=12, slowperiod=26, signalperiod=9)
        macddf = {'macd':macd[0],'macdsignal':macd[1],'macdhist':macd[2]}
        return pd.DataFrame(macddf,index=self.__Tickdata.index)

    def MACDEXT(self):
        # macd, macdsignal, macdhist = MACDEXT(close, fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0, signalperiod=9, signalmatype=0)
        macdext = ta.MACDEXT(self.__Tickdata['close'].values,fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0, signalperiod=9, signalmatype=0)
        macdextdf = {'macdext':macdext[0],'macdsignalext':macdext[1],'macdhistext':macdext[2]}
        return pd.DataFrame(macdextdf,index=self.__Tickdata.index)

    def MFI(self):
        # real = MFI(high, low, close, volume, timeperiod=14)
        mfi = ta.MFI(self.__Tickdata['high'].values, self.__Tickdata['low'].values, self.__Tickdata['close'].values,self.__Tickdata['volume'].values,timeperiod=14)
        return pd.Series(mfi,index=self.__Tickdata.index)

    def MINUS_DI(self):
        # real = MINUS_DI(high, low, close, timeperiod=14)
        minus_di = ta.MINUS_DI(self.__Tickdata['high'].values, self.__Tickdata['low'].values, self.__Tickdata['close'].values,timeperiod=14)
        return pd.Series(minus_di,index=self.__Tickdata.index)

    def MINUS_DM(self):
        # real = MINUS_DM(high, low, timeperiod=14)
        minus_dm = ta.MINUS_DM(self.__Tickdata['high'].values, self.__Tickdata['low'].values,timeperiod=14)
        return pd.Series(minus_dm,index=self.__Tickdata.index)



    def data_assemble(self, datelist):
        # assemble all the data
        TickDataFrame = pd.DataFrame(index=self.__Tickdata.index)
        for value in datelist:
            s0 = pd.Series(self.GoodOrBad(self.__Tickdata, self.__uppercent), name='Tick_KGB')
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
            df = pd.concat([s0,s1, s2, s3, s4, s5, s6, s7, s8,s9], axis=1)
            TickDataFrame = pd.concat([TickDataFrame, df], axis=1)
        return TickDataFrame


alist = [5, 10, 30, 60, 90]
Myclass = TaMainFrame('600519', 365, 30, 90, 0.2)
# tmp = dp.init_Tick('000001')
test = Myclass.MFI()
# test = Myclass.GoodOrBad(Tickdf,0.1)
