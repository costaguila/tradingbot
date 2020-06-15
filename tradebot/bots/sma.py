from decimal import Decimal
from tradebot.bots.abstract import AbstractTradebot
from tradebot.datasources.alphavantage import AlphavantageAdapter
from tradebot.market.stock import StockList


class SimpleMovingAverageBot(AbstractTradebot):

    def __init__(self, symbol, useAdapterDefaults=True,
        adapter=AlphavantageAdapter,  debug = True ):
        self.symbol = symbol
        self.datasource = adapter()
        if useAdapterDefaults:
            # O dataframe deve ser do mais antigo para o mais novo
            self.stock_list = StockList(self.datasource.getStocks(self.symbol)[::-1])
        else:
            self.stock_list = StockList([])
        self.debug = debug
        self.moving_avarage15 = self.calculate_moving_average(20)
        self.moving_avarage30 = self.calculate_moving_average(80)

    def __str__(self):
        return "SimpleMovingAverageBot(Symbol:{})".format(self.symbol)

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

    def operate(self):
        """
        Loop principal do robo.
            1. Recuperar os dados mais recentes
            2. Verificar os dados que nao possuimos e adicionar stock_list através do metodo
               stock_list.add(dict).
            3. Atualizar moving_avarage
            4. Se o valor da acao era maior e ficou menor que o moving_avarage
                vender, OU se o valor da acao era menor e ficou maior que o moving_avarage
                comprar.
            5. Sempre utilizar 100% do dinheiro nesse momentos de compra/venda
        """
