import uuid
import requests
'''

spec:


String data = get_data_from_api(name,start_date)

Stock stock = Stock(data)

sim : fn t => $ := stock.simulate(inputs)


...


parse ["BUY date0", "SELL date1", "BUY date2",...] => sim.buy(date0); sim.sell(date1)


}


buy and sell commands update portfolio

so have:

User (name, Portfolio)

Portfolio (Market, holdings, value, cash) : can buy using cash, value is value of holdings + cash, has buy/sell functions that wrap the Stock.buy/sell in holdings (dict Stock)

Market (dict of Stocks)

Stock (single stock): has info, and price function. buy/sell commands take in date, number. also get

'''



#Need to update encapsulation + privacy settings

class Stock:
    def __init__(self,name, ticker, raw_data = None):
        self.name = name
        self.ticker = ticker
        self.raw_data=raw_data
        self.pricefn = lambda t: -1
        self.cache = lambda t: False
    
    def set_pricefn(self, raw_data = None):
        self.raw_data=raw_data
        if(self.raw_data == None):
            return
        
        #parse here!!!!!
        #set pricefn!!!!
        return
    
    def get(self, date):
        return self.pricefn(date)
    
    


class Portfolio:
    def __init__(self, market):
        self.market = market
        self.holdings = dict()
        self.cash = 0

    
    #TODO FIX!!!!
    def buy(self, buyOrder):
        (ticker, date, number) = buyOrder
        price = number * self.holdings[ticker].get(date)
        if (self.cash < price):
            raise ValueError("Insufficient Cash")
        self.cash -= price
        if (ticker in self.holdings.keys()):
            self.holdings[ticker] += number
        else:
            self.holdings[ticker] = number

        

    
    def sell(self, sellOrder):
        (ticker, date, number) = sellOrder
        value = number * self.holdings[ticker].get(date)
        if (ticker not in self.holdings.keys()):
            raise KeyError("Ticker Not Found")
        
        if (self.holdings[ticker] < number):
            raise ValueError("Insufficient Cash")
        
        self += value
        self.holdings[ticker] -= number
        if (self.holdings[ticker] == 0):
            del self.holdings[ticker]
        

        


class UserInfo:
    def __init__(self, name):
        self.name = name
        self.id = uuid.uuid4()
    

class User:
    def __init__(self, user_info, Portfolio):
        self.info = user_info
        self.portfolio = Portfolio
    
    