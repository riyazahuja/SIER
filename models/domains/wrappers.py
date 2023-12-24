class Stock:
    def __init__(self, name, ticker, price_service):
        self.name = name
        self.ticker = ticker
        self.price_service = price_service

    def get_price(self, date):
        return self.price_service.get_price(self.ticker, date)


class Portfolio:
    def __init__(self):
        self.holdings = {}  # Ticker to quantity
        self.cash = 0  # Initial cash

    def buy(self, ticker, date, quantity, stock):
        price = quantity * stock.get_price(date)
        if self.cash < price:
            raise ValueError("Insufficient cash for transaction.")
        self.cash -= price
        self.holdings[ticker] = self.holdings.get(ticker, 0) + quantity

    def sell(self, ticker, date, quantity, stock):
        if ticker not in self.holdings or self.holdings[ticker] < quantity:
            raise ValueError("Insufficient shares to sell.")
        price = quantity * stock.get_price(date)
        self.holdings[ticker] -= quantity
        if self.holdings[ticker] == 0:
            del self.holdings[ticker]
        self.cash += price
