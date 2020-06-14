from decimal import Decimal
from tradebot.bots.abstract import AbstractTradebot
from tradebot.datasources.alphavantage import AlphavantageAdapter
from tradebot.market.stock import Stock
from tradebot.market.metrics import movingAverage

class SimpleMovingAverageBot(AbstractTradebot):

    def __init__(self, symbol, useAdapterDefaults=True,
        adapter=AlphavantageAdapter,  debug = True ):
        self.symbol = symbol
        self.datasource = adapter()
        if useAdapterDefaults:
            self.stock_list = self.datasource.getStocks(self.symbol)
        else:
            self.stock_list = []
        self.debug = debug
        self.moving_avarage15 = self.calculate_moving_average(10)
        self.moving_avarage30 = self.calculate_moving_average(20)


    def __str__(self):
        return "SimpleMovingAverageBot(Symbol:{})".format(self.symbol)

    def calculate_moving_average(self, window=None):
        window = len(self.stock_list) - 1 if not window else int(window)

        moving_average = movingAverage(self.stock_list, window)

        if self.debug:
            self.log({
                'operation': 'Calculating moving average for date {}'.format(self.stock_list[0].read_date),
                'moving_average': 'Moving average is {}'.format(moving_average),
                'window': 'moving_avarage is based on {} records'.format(window)
            })
        return moving_average
