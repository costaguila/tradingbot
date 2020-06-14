import os
import requests
from decimal import Decimal
from datetime import datetime
from tradebot.market.stock import Stock
from tradebot.datasources.abstract import AbstractAdapter

class AlphavantageAdapter(AbstractAdapter):
    TIME_SERIES_INTRADAY = 'TIME_SERIES_INTRADAY'
    TIME_SERIES_DAILY = 'TIME_SERIES_DAILY'
    TIME_SERIES_WEEKLY = 'TIME_SERIES_WEEKLY'
    TIME_SERIES_MONTHLY = 'TIME_SERIES_MONTHLY'

    URL = 'https://www.alphavantage.co/query?'
    RESULT_KEY = {
        TIME_SERIES_INTRADAY: 'Time Series (interval)',
        TIME_SERIES_DAILY: 'Time Series (Daily)',
        TIME_SERIES_WEEKLY: 'Weekly Time Series',
        TIME_SERIES_MONTHLY: 'Monthly Time Series'
    }

    def getStocks(self, symbol, period=TIME_SERIES_WEEKLY, interval='5min'):
        apikey = os.getenv('ALPHAVANTAGE_KEY', '')
        ENDPOINT = self.URL+f'function={period}&symbol={symbol}&apikey={apikey}'
        # A chave dos resultados muda dependendo da série temporal usada
        result_key = self.RESULT_KEY[period]
        if period == self.TIME_SERIES_INTRADAY:
            ENDPOINT += f"&interval={interval}"
            result_key = result_key.replace('interval', interval)

        response = requests.get(ENDPOINT)
        if response.status_code == 200:
            result = []
            data = response.json()

            for item in data[result_key].keys():
                open = Decimal(data[result_key][item]['1. open'])
                high = Decimal(data[result_key][item]['2. high'])
                low = Decimal(data[result_key][item]['3. low'])
                close = Decimal(data[result_key][item]['4. close'])
                volume = Decimal(data[result_key][item]['5. volume'])

                try:
                    datetime_obj = datetime.strptime(item, '%Y-%m-%d %H:%M:%S')
                except:
                    datetime_obj = datetime.strptime(item, '%Y-%m-%d')

                result.append(Stock(open=open,high=high,low=low, close=close,
                    volume=volume, date_time=datetime_obj))
        else:
            result = []

        return result
