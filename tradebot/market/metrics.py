from decimal import Decimal

def movingAverage(stock_list=[], window=10):
    """
     Calcula a média da segunda ação até window.
    """
    average = Decimal(0.0)
    sum = Decimal(0.0)
    # inclui o elemento da posicao window
    for stock in stock_list[1:window+1]:
        sum += stock.close

    average = Decimal(sum/window)
    return average
