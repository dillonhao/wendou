class MacroEconomics(object):
    def __init__(self, instrument, timewindow):
        self.__instrument = instrument
        self.__timewindow = int(timewindow)
        self.__starttime = (datetime.datetime.now() - datetime.timedelta(days=self.__timewindow)).strftime('%Y-%m-%d')
        # __starttime is max time of entry point
        self.__endtime = datetime.datetime.now().strftime('%Y-%m-%d')