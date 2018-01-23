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

# Volume Indicator Functions
    def AD(self):
        # real = AD(high, low, close, volume)
        ad = ta.AD(self.__Tickdata['high'].values, self.__Tickdata['low'].values, self.__Tickdata['close'].values,self.__Tickdata['volume'].values)
        return pd.Series(ad, index=self.__Tickdata.index)

    def ADOSC(self):
        # real = ADOSC(high, low, close, volume, fastperiod=3, slowperiod=10)
        adosc = ta.ADOSC(self.__Tickdata['high'].values, self.__Tickdata['low'].values, self.__Tickdata['close'].values,self.__Tickdata['volume'].values, fastperiod=3,slowperiod=10)
        return pd.Series(adosc, index=self.__Tickdata.index)

    def OBV(self):
        # real = OBV(close, volume)
        obv = ta.OBV( self.__Tickdata['close'].values,self.__Tickdata['volume'].values)
        return pd.Series(obv, index=self.__Tickdata.index)

## Volatility Indicator Functions
    def ATR(self):
        # real = ATR(high, low, close, timeperiod=14)
        atr = ta.ATR(self.__Tickdata['high'].values, self.__Tickdata['low'].values, self.__Tickdata['close'].values,timeperiod=14)
        return pd.Series(atr, index=self.__Tickdata.index)

    def NATR(self):
        # real = NATR(high, low, close, timeperiod=14)
        natr = ta.NATR(self.__Tickdata['high'].values, self.__Tickdata['low'].values, self.__Tickdata['close'].values,timeperiod=14)
        return pd.Series(natr, index=self.__Tickdata.index)

    def TRANGE(self):
        # real = TRANGE(high, low, close)
        trange = ta.TRANGE(self.__Tickdata['high'].values, self.__Tickdata['low'].values, self.__Tickdata['close'].values)
        return pd.Series(trange, index=self.__Tickdata.index)

    def AVGPRICE(self):
        # real = AVGPRICE(open, high, low, close)
        avgprice = ta.AVGPRICE(self.__Tickdata['open'].values,self.__Tickdata['high'].values, self.__Tickdata['low'].values, self.__Tickdata['close'].values)
        return pd.Series(avgprice, index=self.__Tickdata.index)

    def MEDPRICE(self):
        # real = MEDPRICE(high, low)
        medprice = ta.MEDPRICE(self.__Tickdata['high'].values, self.__Tickdata['low'].values)
        return pd.Series(medprice, index=self.__Tickdata.index)

    def TYPPRICE(self):
        # real = TYPPRICE(high, low, close)
        typprice = ta.TYPPRICE(self.__Tickdata['high'].values, self.__Tickdata['low'].values, self.__Tickdata['close'].values)
        return pd.Series(typprice, index=self.__Tickdata.index)

    def WCLPRICE(self):
        # real = WCLPRICE(high, low, close)
        wclprice = ta.WCLPRICE(self.__Tickdata['high'].values, self.__Tickdata['low'].values, self.__Tickdata['close'].values)
        return pd.Series(wclprice, index=self.__Tickdata.index)

# Cycle Indicator Functions
    def HT_DCPERIOD(self):
        # real = HT_DCPERIOD(close)
        ht_dcperiod = ta.HT_DCPERIOD(self.__Tickdata['close'].values)
        return pd.Series(ht_dcperiod, index=self.__Tickdata.index)

    def HT_DCPHASE(self):
        # real = HT_DCPHASE(close)
        ht_dcphase = ta.HT_DCPHASE(self.__Tickdata['close'].values)
        return pd.Series(ht_dcphase, index=self.__Tickdata.index)

    def HT_PHASOR(self):
        # inphase, quadrature = HT_PHASOR(close)
        inphase, quadrature = ta.HT_PHASOR(self.__Tickdata['close'].values)
        return pd.DataFrame({'inphase':inphase,'quadrature':quadrature},index=self.__Tickdata.index)

    def HT_SINE(self):
        sine, leadsine = HT_SINE(self.__Tickdata['close'].values)
        return pd.DataFrame({'sine':sine,'leadsine':leadsine},index=self.__Tickdata.index)

    def HT_TRENDMODE(self):
        integer = HT_TRENDMODE(self.__Tickdata['close'].values)
        return pd.Series(integer, index=self.__Tickdata.index)

    def Pattern_Recognition_Functions(self):
        open = self.__Tickdata['open'].values
        high = self.__Tickdata['high'].values
        low = self.__Tickdata['low'].values
        close = self.__Tickdata['close'].values
        volume = self.__Tickdata['volume'].values
        upperband, middleband, lowerband = ta.BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
        DEMA = ta.DEMA(close, timeperiod=30)
        EMA = ta.EMA(close, timeperiod=30)
        HT_TRENDLINE = ta.HT_TRENDLINE(close)
        KAMA = ta.KAMA(close, timeperiod=30)
        MA = ta.MA(close, timeperiod=30, matype=0)
        #mama, fama = ta.MAMA(close, fastlimit=0, slowlimit=0)
        #MAVP = ta.MAVP(close, periods, minperiod=2, maxperiod=30, matype=0)
        MIDPOINT = ta.MIDPOINT(close, timeperiod=14)
        MIDPRICE = ta.MIDPRICE(high, low, timeperiod=14)
        SAR = ta.SAR(high, low, acceleration=0, maximum=0)
        SAREXT = ta.SAREXT(high, low, startvalue=0, offsetonreverse=0, accelerationinitlong=0, accelerationlong=0,
                           accelerationmaxlong=0, accelerationinitshort=0, accelerationshort=0, accelerationmaxshort=0)
        SMA = ta.SMA(close, timeperiod=30)
        T3 = ta.T3(close, timeperiod=5, vfactor=0)
        TEMA = ta.TEMA(close, timeperiod=30)
        TRIMA = ta.TRIMA(close, timeperiod=30)
        WMA = ta.WMA(close, timeperiod=30)
        ADX = ta.ADX(high, low, close, timeperiod=14)
        ADXR = ta.ADXR(high, low, close, timeperiod=14)
        APO = ta.APO(close, fastperiod=12, slowperiod=26, matype=0)
        aroondown, aroonup = ta.AROON(high, low, timeperiod=14)
        AROONOSC = ta.AROONOSC(high, low, timeperiod=14)
        BOP = ta.BOP(open, high, low, close)
        CCI = ta.CCI(high, low, close, timeperiod=14)
        CMO = ta.CMO(close, timeperiod=14)
        DX = ta.DX(high, low, close, timeperiod=14)
        macd, macdsignal, macdhist = ta.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
        macdEXT, macdsignalEXT, macdhistEXT = ta.MACDEXT(close, fastperiod=12, fastmatype=0, slowperiod=26,
                                                         slowmatype=0, signalperiod=9, signalmatype=0)
        macdFIX, macdsignalFIX, macdhistFIX = ta.MACDFIX(close, signalperiod=9)
        MFI = ta.MFI(high, low, close, volume, timeperiod=14)
        MINUS_DI = ta.MINUS_DI(high, low, close, timeperiod=14)
        MINUS_DM = ta.MINUS_DM(high, low, timeperiod=14)
        MOM = ta.MOM(close, timeperiod=10)
        PLUS_DI = ta.PLUS_DI(high, low, close, timeperiod=14)
        PLUS_DM = ta.PLUS_DM(high, low, timeperiod=14)
        PPO = ta.PPO(close, fastperiod=12, slowperiod=26, matype=0)
        ROC = ta.ROC(close, timeperiod=10)
        ROCP = ta.ROCP(close, timeperiod=10)
        ROCR = ta.ROCR(close, timeperiod=10)
        ROCR100 = ta.ROCR100(close, timeperiod=10)
        RSI = ta.RSI(close, timeperiod=14)
        slowk, slowd = ta.STOCH(high, low, close, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3,
                                slowd_matype=0)
        fastkF, fastdF = ta.STOCHF(high, low, close, fastk_period=5, fastd_period=3, fastd_matype=0)
        fastkRSI, fastdRSI = ta.STOCHRSI(close, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
        TRIX = ta.TRIX(close, timeperiod=30)
        ULTOSC = ta.ULTOSC(high, low, close, timeperiod1=7, timeperiod2=14, timeperiod3=28)
        WILLR = ta.WILLR(high, low, close, timeperiod=14)
        AD = ta.AD(high, low, close, volume)
        ADOSC = ta.ADOSC(high, low, close, volume, fastperiod=3, slowperiod=10)
        OBV = ta.OBV(close, volume)
        ATR = ta.ATR(high, low, close, timeperiod=14)
        NATR = ta.NATR(high, low, close, timeperiod=14)
        TRANGE = ta.TRANGE(high, low, close)
        AVGPRICE = ta.AVGPRICE(open, high, low, close)
        MEDPRICE = ta.MEDPRICE(high, low)
        TYPPRICE = ta.TYPPRICE(high, low, close)
        WCLPRICE = ta.WCLPRICE(high, low, close)
        HT_DCPERIOD = ta.HT_DCPERIOD(close)
        HT_DCPHASE = ta.HT_DCPHASE(close)
        inphase, quadrature = ta.HT_PHASOR(close)
        sine, leadsine = ta.HT_SINE(close)
        HT_TRENDMODE = ta.HT_TRENDMODE(close)
        CDL2CROWS = ta.CDL2CROWS(open, high, low, close)
        CDL3BLACKCROWS = ta.CDL3BLACKCROWS(open, high, low, close)
        CDL3INSIDE = ta.CDL3INSIDE(open, high, low, close)
        CDL3LINESTRIKE = ta.CDL3LINESTRIKE(open, high, low, close)
        CDL3OUTSIDE = ta.CDL3OUTSIDE(open, high, low, close)
        CDL3STARSINSOUTH = ta.CDL3STARSINSOUTH(open, high, low, close)
        CDL3WHITESOLDIERS = ta.CDL3WHITESOLDIERS(open, high, low, close)
        CDLABANDONEDBABY = ta.CDLABANDONEDBABY(open, high, low, close, penetration=0)
        CDLADVANCEBLOCK = ta.CDLADVANCEBLOCK(open, high, low, close)
        CDLBELTHOLD = ta.CDLBELTHOLD(open, high, low, close)
        CDLBREAKAWAY = ta.CDLBREAKAWAY(open, high, low, close)
        CDLCLOSINGMARUBOZU = ta.CDLCLOSINGMARUBOZU(open, high, low, close)
        CDLCONCEALBABYSWALL = ta.CDLCONCEALBABYSWALL(open, high, low, close)
        CDLCOUNTERATTACK = ta.CDLCOUNTERATTACK(open, high, low, close)
        CDLDARKCLOUDCOVER = ta.CDLDARKCLOUDCOVER(open, high, low, close, penetration=0)
        CDLDOJI = ta.CDLDOJI(open, high, low, close)
        CDLDOJISTAR = ta.CDLDOJISTAR(open, high, low, close)
        CDLDRAGONFLYDOJI = ta.CDLDRAGONFLYDOJI(open, high, low, close)
        CDLENGULFING = ta.CDLENGULFING(open, high, low, close)
        CDLEVENINGDOJISTAR = ta.CDLEVENINGDOJISTAR(open, high, low, close, penetration=0)
        CDLEVENINGSTAR = ta.CDLEVENINGSTAR(open, high, low, close, penetration=0)
        CDLGAPSIDESIDEWHITE = ta.CDLGAPSIDESIDEWHITE(open, high, low, close)
        CDLGRAVESTONEDOJI = ta.CDLGRAVESTONEDOJI(open, high, low, close)
        CDLHAMMER = ta.CDLHAMMER(open, high, low, close)
        CDLHANGINGMAN = ta.CDLHANGINGMAN(open, high, low, close)
        CDLHARAMI = ta.CDLHARAMI(open, high, low, close)
        CDLHARAMICROSS = ta.CDLHARAMICROSS(open, high, low, close)
        CDLHIGHWAVE = ta.CDLHIGHWAVE(open, high, low, close)
        CDLHIKKAKE = ta.CDLHIKKAKE(open, high, low, close)
        CDLHIKKAKEMOD = ta.CDLHIKKAKEMOD(open, high, low, close)
        CDLHOMINGPIGEON = ta.CDLHOMINGPIGEON(open, high, low, close)
        CDLIDENTICAL3CROWS = ta.CDLIDENTICAL3CROWS(open, high, low, close)
        CDLINNECK = ta.CDLINNECK(open, high, low, close)
        CDLINVERTEDHAMMER = ta.CDLINVERTEDHAMMER(open, high, low, close)
        CDLKICKING = ta.CDLKICKING(open, high, low, close)
        CDLKICKINGBYLENGTH = ta.CDLKICKINGBYLENGTH(open, high, low, close)
        CDLLADDERBOTTOM = ta.CDLLADDERBOTTOM(open, high, low, close)
        CDLLONGLEGGEDDOJI = ta.CDLLONGLEGGEDDOJI(open, high, low, close)
        CDLLONGLINE = ta.CDLLONGLINE(open, high, low, close)
        CDLMARUBOZU = ta.CDLMARUBOZU(open, high, low, close)
        CDLMATCHINGLOW = ta.CDLMATCHINGLOW(open, high, low, close)
        CDLMATHOLD = ta.CDLMATHOLD(open, high, low, close, penetration=0)
        CDLMORNINGDOJISTAR = ta.CDLMORNINGDOJISTAR(open, high, low, close, penetration=0)
        CDLMORNINGSTAR = ta.CDLMORNINGSTAR(open, high, low, close, penetration=0)
        CDLONNECK = ta.CDLONNECK(open, high, low, close)
        CDLPIERCING = ta.CDLPIERCING(open, high, low, close)
        CDLRICKSHAWMAN = ta.CDLRICKSHAWMAN(open, high, low, close)
        CDLRISEFALL3METHODS = ta.CDLRISEFALL3METHODS(open, high, low, close)
        CDLSEPARATINGLINES = ta.CDLSEPARATINGLINES(open, high, low, close)
        CDLSHOOTINGSTAR = ta.CDLSHOOTINGSTAR(open, high, low, close)
        CDLSHORTLINE = ta.CDLSHORTLINE(open, high, low, close)
        CDLSPINNINGTOP = ta.CDLSPINNINGTOP(open, high, low, close)
        CDLSTALLEDPATTERN = ta.CDLSTALLEDPATTERN(open, high, low, close)
        CDLSTICKSANDWICH = ta.CDLSTICKSANDWICH(open, high, low, close)
        CDLTAKURI = ta.CDLTAKURI(open, high, low, close)
        CDLTASUKIGAP = ta.CDLTASUKIGAP(open, high, low, close)
        CDLTHRUSTING = ta.CDLTHRUSTING(open, high, low, close)
        CDLTRISTAR = ta.CDLTRISTAR(open, high, low, close)
        CDLUNIQUE3RIVER = ta.CDLUNIQUE3RIVER(open, high, low, close)
        CDLUPSIDEGAP2CROWS = ta.CDLUPSIDEGAP2CROWS(open, high, low, close)
        CDLXSIDEGAP3METHODS = ta.CDLXSIDEGAP3METHODS(open, high, low, close)
        BETA = ta.BETA(high, low, timeperiod=5)
        CORREL = ta.CORREL(high, low, timeperiod=30)
        LINEARREG = ta.LINEARREG(close, timeperiod=14)
        LINEARREG_ANGLE = ta.LINEARREG_ANGLE(close, timeperiod=14)
        LINEARREG_INTERCEPT = ta.LINEARREG_INTERCEPT(close, timeperiod=14)
        LINEARREG_SLOPE = ta.LINEARREG_SLOPE(close, timeperiod=14)
        STDDEV = ta.STDDEV(close, timeperiod=5, nbdev=1)
        TSF = ta.TSF(close, timeperiod=14)
        VAR = ta.VAR(close, timeperiod=5, nbdev=1)
        tadf = pd.DataFrame({
            'upperband': upperband,
            'middleband': middleband,
            'lowerband': lowerband,
            'DEMA': DEMA,
            'EMA': EMA,
            'HT_TRENDLINE': HT_TRENDLINE,
            'KAMA': KAMA,
            'MA': MA,
            'MIDPOINT': MIDPOINT,
            'MIDPRICE': MIDPRICE,
            'SAR': SAR,
            'SAREXT': SAREXT,
            'SMA': SMA,
            'T3': T3,
            'TEMA': TEMA,
            'TRIMA': TRIMA,
            'WMA': WMA,
            'ADX': ADX,
            'ADXR': ADXR,
            'APO': APO,
            'aroondown': aroondown,
            'aroonup': aroonup,
            'AROONOSC': AROONOSC,
            'BOP': BOP,
            'CCI': CCI,
            'CMO': CMO,
            'DX': DX,
            'macd': macd,
            'macdsignal': macdsignal,
            'macdhist': macdhist,
            'macdEXT': macdEXT,
            'macdsignalEXT': macdsignalEXT,
            'macdhistEXT': macdhistEXT,
            'macdFIX': macdFIX,
            'macdsignalFIX': macdsignalFIX,
            'macdhistFIX': macdhistFIX,
            'MFI': MFI,
            'MINUS_DI': MINUS_DI,
            'MINUS_DM': MINUS_DM,
            'MOM': MOM,
            'PLUS_DI': PLUS_DI,
            'PLUS_DM': PLUS_DM,
            'PPO': PPO,
            'ROC': ROC,
            'ROCP': ROCP,
            'ROCR': ROCR,
            'ROCR100': ROCR100,
            'RSI': RSI,
            'slowk': slowk,
            'slowd': slowd,
            'fastkF': fastkF,
            'fastdF': fastdF,
            'fastkRSI': fastkRSI,
            'fastdRSI': fastdRSI,
            'TRIX': TRIX,
            'ULTOSC': ULTOSC,
            'WILLR': WILLR,
            'AD': AD,
            'ADOSC': ADOSC,
            'OBV': OBV,
            'ATR': ATR,
            'NATR': NATR,
            'TRANGE': TRANGE,
            'AVGPRICE': AVGPRICE,
            'MEDPRICE': MEDPRICE,
            'TYPPRICE': TYPPRICE,
            'WCLPRICE': WCLPRICE,
            'HT_DCPERIOD': HT_DCPERIOD,
            'HT_DCPHASE': HT_DCPHASE,
            'inphase': inphase,
            'quadrature': quadrature,
            'sine': sine,
            'leadsine': leadsine,
            'HT_TRENDMODE': HT_TRENDMODE,
            'CDL2CROWS': CDL2CROWS,
            'CDL3BLACKCROWS': CDL3BLACKCROWS,
            'CDL3INSIDE': CDL3INSIDE,
            'CDL3LINESTRIKE': CDL3LINESTRIKE,
            'CDL3OUTSIDE': CDL3OUTSIDE,
            'CDL3STARSINSOUTH': CDL3STARSINSOUTH,
            'CDL3WHITESOLDIERS': CDL3WHITESOLDIERS,
            'CDLABANDONEDBABY': CDLABANDONEDBABY,
            'CDLADVANCEBLOCK': CDLADVANCEBLOCK,
            'CDLBELTHOLD': CDLBELTHOLD,
            'CDLBREAKAWAY': CDLBREAKAWAY,
            'CDLCLOSINGMARUBOZU': CDLCLOSINGMARUBOZU,
            'CDLCONCEALBABYSWALL': CDLCONCEALBABYSWALL,
            'CDLCOUNTERATTACK': CDLCOUNTERATTACK,
            'CDLDARKCLOUDCOVER': CDLDARKCLOUDCOVER,
            'CDLDOJI': CDLDOJI,
            'CDLDOJISTAR': CDLDOJISTAR,
            'CDLDRAGONFLYDOJI': CDLDRAGONFLYDOJI,
            'CDLENGULFING': CDLENGULFING,
            'CDLEVENINGDOJISTAR': CDLEVENINGDOJISTAR,
            'CDLEVENINGSTAR': CDLEVENINGSTAR,
            'CDLGAPSIDESIDEWHITE': CDLGAPSIDESIDEWHITE,
            'CDLGRAVESTONEDOJI': CDLGRAVESTONEDOJI,
            'CDLHAMMER': CDLHAMMER,
            'CDLHANGINGMAN': CDLHANGINGMAN,
            'CDLHARAMI': CDLHARAMI,
            'CDLHARAMICROSS': CDLHARAMICROSS,
            'CDLHIGHWAVE': CDLHIGHWAVE,
            'CDLHIKKAKE': CDLHIKKAKE,
            'CDLHIKKAKEMOD': CDLHIKKAKEMOD,
            'CDLHOMINGPIGEON': CDLHOMINGPIGEON,
            'CDLIDENTICAL3CROWS': CDLIDENTICAL3CROWS,
            'CDLINNECK': CDLINNECK,
            'CDLINVERTEDHAMMER': CDLINVERTEDHAMMER,
            'CDLKICKING': CDLKICKING,
            'CDLKICKINGBYLENGTH': CDLKICKINGBYLENGTH,
            'CDLLADDERBOTTOM': CDLLADDERBOTTOM,
            'CDLLONGLEGGEDDOJI': CDLLONGLEGGEDDOJI,
            'CDLLONGLINE': CDLLONGLINE,
            'CDLMARUBOZU': CDLMARUBOZU,
            'CDLMATCHINGLOW': CDLMATCHINGLOW,
            'CDLMATHOLD': CDLMATHOLD,
            'CDLMORNINGDOJISTAR': CDLMORNINGDOJISTAR,
            'CDLMORNINGSTAR': CDLMORNINGSTAR,
            'CDLONNECK': CDLONNECK,
            'CDLPIERCING': CDLPIERCING,
            'CDLRICKSHAWMAN': CDLRICKSHAWMAN,
            'CDLRISEFALL3METHODS': CDLRISEFALL3METHODS,
            'CDLSEPARATINGLINES': CDLSEPARATINGLINES,
            'CDLSHOOTINGSTAR': CDLSHOOTINGSTAR,
            'CDLSHORTLINE': CDLSHORTLINE,
            'CDLSPINNINGTOP': CDLSPINNINGTOP,
            'CDLSTALLEDPATTERN': CDLSTALLEDPATTERN,
            'CDLSTICKSANDWICH': CDLSTICKSANDWICH,
            'CDLTAKURI': CDLTAKURI,
            'CDLTASUKIGAP': CDLTASUKIGAP,
            'CDLTHRUSTING': CDLTHRUSTING,
            'CDLTRISTAR': CDLTRISTAR,
            'CDLUNIQUE3RIVER': CDLUNIQUE3RIVER,
            'CDLUPSIDEGAP2CROWS': CDLUPSIDEGAP2CROWS,
            'CDLXSIDEGAP3METHODS': CDLXSIDEGAP3METHODS,
            'BETA': BETA,
            'CORREL': CORREL,
            'LINEARREG': LINEARREG,
            'LINEARREG_ANGLE': LINEARREG_ANGLE,
            'LINEARREG_INTERCEPT': LINEARREG_INTERCEPT,
            'LINEARREG_SLOPE': LINEARREG_SLOPE,
            'STDDEV': STDDEV,
            'TSF': TSF,
            'VAR': VAR
        },index=self.__Tickdata.index)
        return tadf
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
test7 = Myclass.Pattern_Recognition_Functions()
# test = Myclass.GoodOrBad(Tickdf,0.1)
