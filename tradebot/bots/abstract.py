from datetime import datetime
class AbstractTradebot:
    OPERACAO_COMPRA = 'COMPRA'
    OPERACAO_VENDA = 'VENDA'
    OPERACAO_MANTER = 'MANTER'
    def __init__(self):
        pass

    def __str__(self):
        pass

    def evaluate(self, stock):
        pass

    def operate(self):
        pass

    def log(self, log_dictionary):
        for item in log_dictionary.keys():
            print("[{} {}]  {}".format( datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M:%S'), self, str(log_dictionary[item]) ))
        print('')
