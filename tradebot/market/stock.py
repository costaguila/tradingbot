import pandas as pd

class StockList:
    """
        Representa uma lista de ações de uma empresa, DEVE estar ordenadas da
        mais antiga para a mais recente.
        Formato do dataframe:
            {
            'open':open,        # Valor durante a abertura
            'high':high,        # Valor mais alto daquela data/hora
            'low':low,          # Valor mais baixo daquela data/hora
            'close':close,      # Valor de fechamento daquela data/hora
            'volume':volume,    # Volume negociado
            'date':date,        # Data em que o valor foi recuperado
            'time':time         # Valor durante a abertura
            }
    """
    def __init__(self, stock_list):
        self.dataframe = pd.DataFrame(stock_list)

    def add(self, stock):
         data = self.dataframe.append(stock, ignore_index=True)
         self.dataframe = data
