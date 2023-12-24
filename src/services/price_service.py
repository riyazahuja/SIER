import requests
from ..utils.cache import Cache
import os

POLYGON_API_KEY = os.genenv('POLYGON_API_KEY')

class PriceService:
    def __init__(self, api_key = POLYGON_API_KEY, cache_size = 4096):
        self.api_key = api_key
        self.cache = Cache(cache_size)

    def fetch_price_from_polygon(self, ticker, date):
        # Implement the actual API call to Polygon.io here
        # and return the price data.
        pass

    def get_price(self, ticker, date):
        # Check cache first
        cached_price = self.cache.get((ticker, date))
        if cached_price is not None:
            return cached_price

        # Fetch from API if not cached
        price = self.fetch_price_from_polygon(ticker, date)
        self.cache.put((ticker, date), price)
        return price
