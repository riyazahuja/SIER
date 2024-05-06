import os
import django
import json
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')
django.setup()

from stocks.models import Stock, Price

# Load JSON data
with open('../data/processed/data.json', 'r') as file:
    data = json.load(file)



# Import data
for symbol, details in data.items():
    # Create or update Stock


    stock_keys = ['Name','AssetType','Description','CIK','Currency','Country','Sector','Industry','Address','FiscalYearEnd','LatestQuarter']

    stock, created = Stock.objects.update_or_create(
        symbol=symbol,
        defaults={
            'name': details['Overview']['Name'],
            'asset_type': details['Overview']['AssetType'],
            'description': details['Overview']['Description'],
            'CIK': details['Overview']['CIK'],
            'currency': details['Overview']['Currency'],
            'country': details['Overview']['Country'],
            'sector': details['Overview']['Sector'],
            'industry': details['Overview']['Industry'],
            'address': details['Overview']['Address'],
            'fiscal_year_end': details['Overview']['FiscalYearEnd'],
            'latest_quarter': details['Overview']['LatestQuarter'],
            'data': {k:details['Overview'][k] for k in details['Overview'].keys() if k not in stock_keys}# Storing entire overview as JSON
        }
    )

    # Import Price data
    for date_str, price_data in details['Time Series (Daily)'].items():
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        Price.objects.update_or_create(
            stock=stock,
            date=date,
            defaults={
                'o': price_data['open'],
                'h': price_data['high'],
                'l': price_data['low'],
                'c': price_data['close'],
                'v': price_data['volume'],
                'data': {k:price_data[k] for k in price_data.keys() if k not in ['open','high','low','close','volume']}
            }
        )

print("Data import complete!")
