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

    def MOM(self):
        # real = MOM(close, timeperiod=10)
        mom = ta.MOM(self.__Tickdata['close'].values,timeperiod=10)
        return pd.Series(mom,index=self.__Tickdata.index)

    def PLUS_DI(self):
        # real = PLUS_DI(high, low, close, timeperiod=14)
        plus_di = ta.PLUS_DI(self.__Tickdata['high'].values, self.__Tickdata['low'].values, self.__Tickdata['close'].values,timeperiod=14)
        return pd.Series(plus_di, index=self.__Tickdata.index)

    def PLUS_DM(self):
        # real = PLUS_DM(high, low, timeperiod=14)
        plus_dm = ta.PLUS_DM(self.__Tickdata['high'].values, self.__Tickdata['low'].values,timeperiod=14 )
        return pd.Series(plus_dm, index=self.__Tickdata.index)


    def PPO(self):
        # real = PPO(close, fastperiod=12, slowperiod=26, matype=0)
        ppo = ta.PPO(self.__Tickdata['close'].values,fastperiod=12, slowperiod=26, matype=0)
        return pd.Series(ppo, index=self.__Tickdata.index)

    def ROC(self):
        # real = ROC(close, timeperiod=10)
        roc = ta.ROC(self.__Tickdata['close'].values,timeperiod=10)
        return pd.Series(roc, index=self.__Tickdata.index)

    def ROCP(self):
        # real = ROCP(close, timeperiod=10)
        rocp = ta.ROCP(self.__Tickdata['close'].values,timeperiod=10)
        return pd.Series(rocp, index=self.__Tickdata.index)

    def ROCR(self):
        # real = ROCR(close, timeperiod=10)
        rocr = ta.ROCR(self.__Tickdata['close'].values,timeperiod=10)
        return pd.Series(rocr, index=self.__Tickdata.index)

    def RSI(self):
        # real = RSI(close, timeperiod=14)
        rsi = ta.RSI(self.__Tickdata['close'].values,timeperiod=14)
        return pd.Series(rsi, index=self.__Tickdata.index)

    def STOCH(self):
        # slowk, slowd = STOCH(high, low, close, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
        stoch = ta.STOCH(self.__Tickdata['high'].values, self.__Tickdata['low'].values, self.__Tickdata['close'].values,fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
        stochdf = {'slowk':stoch[0],'slowd':stoch[1]}
        return pd.DataFrame(stochdf, index=self.__Tickdata.index)

    def STOCHF(self):
        # fastk, fastd = STOCHF(high, low, close, fastk_period=5, fastd_period=3, fastd_matype=0)
        stochf = ta.STOCHF(self.__Tickdata['high'].values, self.__Tickdata['low'].values, self.__Tickdata['close'].values,fastk_period=5, fastd_period=3, fastd_matype=0)
        stochfdf = {'fastk':stochf[0],'fastd':stochf[1]}
        return pd.DataFrame(stochfdf, index=self.__Tickdata.index)

    def STOCHRSI(self):
        # fastk, fastd = STOCHRSI(close, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
        stochrsi = ta.STOCHRSI(self.__Tickdata['close'].values,timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
        stochrsidf = {'fastkrsi':stochrsi[0],'fastdrsi':stochrsi[1]}
        return pd.DataFrame(stochrsidf, index=self.__Tickdata.index)

    def TRIX(self):
        # real = TRIX(close, timeperiod=30)
        trix = ta.TRIX(self.__Tickdata['close'].values,timeperiod=30)
        return pd.Series(trix, index=self.__Tickdata.index)


    def ULTOSC(self):
        # real = ULTOSC(high, low, close, timeperiod1=7, timeperiod2=14, timeperiod3=28)
        ultosc = ta.ULTOSC(self.__Tickdata['high'].values, self.__Tickdata['low'].values, self.__Tickdata['close'].values,timeperiod1=7, timeperiod2=14, timeperiod3=28)
        return pd.Series(ultosc, index=self.__Tickdata.index)

    def WILLR(self):
        # real = WILLR(high, low, close, timeperiod=14)
        willr = ta.WILLR(self.__Tickdata['high'].values, self.__Tickdata['low'].values, self.__Tickdata['close'].values,timeperiod=14)
        return pd.Series(willr, index=self.__Tickdata.index)


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
test4 = Myclass.STOCHF()
# test = Myclass.GoodOrBad(Tickdf,0.1)
