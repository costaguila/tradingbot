from decimal import Decimal
import datetime
from tradebot.bots.abstract import AbstractTradebot
from tradebot.datasources.alphavantage import AlphavantageAdapter
from tradebot.market.stock import StockList


class SimpleMovingAverageBot(AbstractTradebot):

    def __init__(self, symbol, window, useAdapterDefaults=True,
        adapter=AlphavantageAdapter,  debug = True ):
        self.symbol = symbol
        self.datasource = adapter()
        if useAdapterDefaults:
            # O dataframe deve ser do mais antigo para o mais novo
            self.stock_list = StockList(self.datasource.getStocks(self.symbol)[::-1])
        else:
            self.stock_list = StockList([])
        self.window = window
        self.debug = debug
        self.moving_avarage = self.calculate_moving_average(window)

    def __str__(self):
        return "SimpleMovingAverageBot(Symbol:{})".format(self.symbol)

    def set_stocks(self, stocks):
        self.stock_list = StockList(stocks)

    def calculate_moving_average(self, window=None):
        window = 10 if not window else int(window)

        moving_average = self.stock_list.dataframe['close'].rolling(window=window).mean()

        if self.debug:
            last_item_date = self.stock_list.dataframe['date'].iloc[-1]
            self.log({
                'operation': 'Calculating moving average for date {}'.format(last_item_date),
                'moving_average': 'Moving average is {}'.format(moving_average.iloc[-1]),
                'window': 'moving_avarage is based on {} records'.format(window)
            })
        return moving_average

    def evaluate(self, stock):
        """
        Loop principal do robo.
            1. Verificar os dados que nao possuimos e adicionar stock_list através do metodo
               stock_list.add(dict).
            2. Atualizar moving_avarage
            3. Se o valor da acao era maior e ficou menor que o moving_avarage
                vender, OU se o valor da acao era menor e ficou maior que o moving_avarage
                comprar.
            4. Sempre utilizar 100% do dinheiro nesse momentos de compra/venda
        """
        #1. Verificar os dados que nao possuimos e adicionar stock_list através do metodo stock_list.add(dict).
        previous_last_item = self.stock_list.dataframe.iloc[-1]

        last_item_date_str = "{} {}".format(
                previous_last_item['date'],
                previous_last_item['time']
            )
        stock_date_str = "{} {}".format(
                stock['date'],
                stock['time']
            )
        last_item_date = datetime.datetime.strptime(last_item_date_str, '%Y-%m-%d %H:%M:%S')
        stock_date = datetime.datetime.strptime(stock_date_str, '%Y-%m-%d %H:%M:%S')

        if stock_date > last_item_date:
            self.stock_list.add(stock)
            self.moving_avarage = self.calculate_moving_average(self.window)
        '''
        3. Se o valor da acao era maior e ficou menor que o moving_avarage
            vender, OU se o valor da acao era menor e ficou maior que o moving_avarage
            comprar.
        '''
        avg = Decimal(self.moving_avarage.iloc[-1])
        if Decimal(previous_last_item['close']) > avg and Decimal(stock['close']) < avg:
            #3. Se o valor da acao era maior e ficou menor que o moving_avarage comprar
            self.log({'valor': Decimal(stock['close']), 'operacao': self.OPERACAO_COMPRA})
            return self.OPERACAO_COMPRA
        elif Decimal(previous_last_item['close']) < avg and Decimal(stock['close']) > avg:
            #3. OU se o valor da acao era menor e ficou maior que o moving_avarage vender.
            self.log({'valor': Decimal(stock['close']), 'operacao': self.OPERACAO_VENDA})
            return self.OPERACAO_VENDA
        else:
            self.log({'valor': Decimal(stock['close']), 'operacao': self.OPERACAO_MANTER})
            return self.OPERACAO_MANTER
