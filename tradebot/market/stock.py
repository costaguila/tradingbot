
class Stock:
    "Represenda uma entrada do gráfico candlestick."
    def __init__(self, open, close, high, low, volume, date_time):
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.volume = volume
        self.read_date = date_time
