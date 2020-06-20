from tradebot.bots.sma import SimpleMovingAverageBot
from tradebot.datasources.alphavantage import AlphavantageAdapter
from tradebot.market.stock import StockList
import time
from decimal import Decimal


def test_sma(symbol="IBM", window=30, bot=SimpleMovingAverageBot, adapter=AlphavantageAdapter):
    test_bot = bot(symbol,window)
    #por padrao recupera de semana em semana
    test_adapter = adapter()
    stocks = test_adapter.getStocks(symbol)[::-1]
    # seprar dados
    # 1 ano = 52 semanas
    previsao  = stocks[-52:]
    test_bot.set_stocks(stocks[:-52])
    test_bot.calculate_moving_average()
    cash = Decimal(1000)
    original_cash = Decimal(cash)
    stocks = 0
    ultima_venda = {
        'CAIXA': f"CAIXA ATUAL= R$ ${cash}",
        'CAIXA ORIGINAL': f"CAIXA ORIGINAL= R${original_cash}",
        'QUANTIDADE DE AÇÕES': f"Qdt AÇÕES NÃO VENDIDAS = {stocks}",
        'VARIAÇÃO CAIXA(%)': f"VARIAÇÃO CAIXA/CAIXA ORIGINAL(%) = 0%"
    }
    for periodo in previsao:
        result = test_bot.evaluate(periodo)
        if result == test_bot.OPERACAO_COMPRA:
            stocks =  cash // periodo['close']
            cash = cash - periodo['close'] * stocks
        elif result == test_bot.OPERACAO_VENDA:
            cash +=  periodo['close'] * stocks
            stocks = 0
            # Monitorar a ultima operacao de venda para avaliar
            # o desempenho do bot SMA
            variacao =  Decimal((cash - original_cash)/original_cash)*Decimal(100)
            ultima_venda = {
                'CAIXA': f"CAIXA ATUAL= R$ ${cash}",
                'CAIXA ORIGINAL': f"CAIXA ORIGINAL= R${original_cash}",
                'QUANTIDADE DE AÇÕES': f"Qdt AÇÕES NÃO VENDIDAS = {stocks}",
                'VARIAÇÃO CAIXA(%)': f"VARIAÇÃO CAIXA/CAIXA ORIGINAL(%) = {variacao}%"
            }
        variacao =  Decimal((cash - original_cash)/original_cash)*Decimal(100)
        test_bot.log({
            'CAIXA': f"CAIXA ATUAL= R$ ${cash}",
            'CAIXA ORIGINAL': f"CAIXA ORIGINAL= R${original_cash}",
            'QUANTIDADE DE AÇÕES': f"Qdt AÇÕES NÃO VENDIDAS = {stocks}",
            'VARIAÇÃO CAIXA(%)': f"VARIAÇÃO CAIXA/CAIXA ORIGINAL(%) = {variacao}%"
        })

        #time.sleep(1)
    print("############ RESULTADO DA ÚLTIMA VENDA ############")
    test_bot.log(ultima_venda)
