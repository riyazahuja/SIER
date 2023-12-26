import requests
from ..utils.cache import Cache
import os
from datetime import datetime, timedelta

STOCK_API_KEY = os.genenv('STOCK_API_KEY')

def is_within_past_100_days(date_str):
        # Format of the date string being passed in, e.g., "2023-01-09"
        date_format = r"%Y-%m-%d"
        
        # Convert the date string to a datetime object
        given_date = datetime.strptime(date_str, date_format)
        
        # Calculate the date 100 days ago from today
        hundred_days_ago = datetime.now() - timedelta(days=100)
        
        # Check if the given date is after the date 100 days ago
        return given_date >= hundred_days_ago


class PriceService:
    def __init__(self, api_key = STOCK_API_KEY, cache_size = 4096):
        self.api_key = api_key
        self.cache = Cache(cache_size)



    def fetch(self, ticker, full_output = False):

        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}{f"&output_size=full" if full_output else ""}&apikey={STOCK_API_KEY}'

        resp = requests.get(url)
        
        if (resp.status_code == 200):

            
            json_data = resp.json
            key = json_data.keys()[-1]
            time_series = json_data[key]
            
            result = dict()
            for k,v in time_series.items():
                obj = dict()
                obj['open'] = float(v['1. open'])
                obj['high'] = float(v['2. high'])
                obj['low'] = float(v['3. low'])
                obj['close'] = float(v['4. close'])
                obj['volume'] = float(v['5. volume'])

                result[k] = obj

            return result
            
        else:
            raise ConnectionError(f"API Request Failed: {resp}")
        


    def get_data(self, ticker, date):
        # Check cache first
        cached_data = self.cache.get((ticker, date))
        if cached_data is not None:
            return cached_data

        # Fetch from API if not cached
        old = is_within_past_100_days(date) #ends up caching EVERYTHING if more than 100 days old is requested.
        time_series = self.fetch(ticker, not old)
        
        for k,v in time_series.items():
            self.cache.put((ticker, k), v)
        return time_series
