from src.services.price_service import PriceService
from src.utils.cache import Cache
from datetime import datetime, date, timedelta

'''
TODO: Fix $PYTHONPATH issue with imports. 
TEMP FIX: Move to root directory before testi
'''




#Test 1: Retrieve AAPL data from 10/31/2023

ps = PriceService()
data = ps.get_data("AAPL", "2023-10-31")
print(f'TEST 1: \n\n{data}\n\n\n')




#Test 2: Retrieve IBM data from today (current date)

today = datetime.today().strftime(r'%Y-%m-%d')

ps = PriceService()
data = ps.get_data("IBM", today)
print(f'TEST 2: \n\n{data}\n\n\n')




#Test 3: Retrieve AAPL data from entire month of November 2023

start = date(2023,11,1)
end = date(2023, 11,30)

delta = timedelta(days=1)

# store the dates between two dates in a list
dates = []

while start <= end:
    # add current date to list by converting  it to iso format
    dates.append(start.strftime(r'%Y-%m-%d'))
    # increment start date by timedelta
    start += delta


ps = PriceService()
closes = dict()
for date in dates:
    data = ps.get_data("IBM", date)
    if data == None:
        closes[date] = None
    else:
        closes[date] = data['close']
print(f'TEST 3: \n\n{closes}\n\n\n')




#Test 4: Retrieve AMZN data from 1/1/2020 (not in past 100 days)


arg = date(2020,1,1).strftime(r'%Y-%m-%d')

ps = PriceService()
data = ps.get_data("AMZN", arg)
print(f'TEST 4: \n\n{data}\n\n\n')

