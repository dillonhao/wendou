import tushare as ts
import pandas as pd
import numpy as np
import datetime
import talib as ta

class MacroEconomics(object):
    def __init__(self, instrument, timewindow):
        self.__instrument = instrument
        self.__timewindow = int(timewindow)
        self.__starttime = (datetime.datetime.now() - datetime.timedelta(days=self.__timewindow)).strftime('%Y-%m-%d')
        # __starttime is max time of entry point
        self.__endtime = datetime.datetime.now().strftime('%Y-%m-%d')
        profit = ts.get_profit_data(2014, 3)
        report = ts.get_report_data(2014, 3)
        operation = ts.get_operation_data(2014, 3)
        growth = ts.get_growth_data(2014, 3)
        debtpay = ts.get_debtpaying_data(2014, 3)
        cashflow = ts.get_cashflow_data(2014, 3)