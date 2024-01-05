from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import JSONField
from datetime import date
# Create your models here.



class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    asset_type = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    CIK = models.BigIntegerField(null=True, blank=True)
    asset_type = models.CharField(max_length=50, null=True, blank=True)
    currency = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    sector = models.CharField(max_length=50, null=True, blank=True)
    industry = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    fiscal_year_end = models.CharField(max_length=50, null=True, blank=True)
    latest_quarter = models.DateField(default = date.today, blank = True)
    data = JSONField(null = True, blank = True)





    def __str__(self):
        return f"{self.symbol} - {self.name}"
    


class Price(models.Model):
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
    date = models.DateField()
    o = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    h = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    l = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    c = models.DecimalField(max_digits=10, decimal_places=2)
    v = models.BigIntegerField(null=True, blank=True)

    data = JSONField(null = True, blank = True)



    def __str__(self):
        return f"{self.stock.symbol} - {self.date} - {self.c}"
    



class Order(models.Model):
    BUY = 'B'
    SELL = 'S'
    ORDER_CHOICES = [
        (BUY, 'Buy'),
        (SELL, 'Sell'),
    ]

    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    shares = models.IntegerField()
    price = models.ForeignKey(Price, on_delete=models.SET_NULL, null=True)
    order_type = models.CharField(
        max_length=1,
        choices=ORDER_CHOICES
    )
    transaction_date = models.DateField()


    def validate_and_set_price(self):
        # Attempt to find a valid price for the given stock and date
        try:
            price = Price.objects.get(stock=self.stock, date=self.transaction_date)
            self.price = price
        except Price.DoesNotExist:
            # No valid price found
            self.price = None

    
    def save(self, *args, **kwargs):
        self.validate_and_set_price()
        super().save(*args, **kwargs)  # Call the "real" save() method.

    def __str__(self):
        return f"{'BUY' if self.order_type == 'B' else 'SELL'} Order: [{self.shares}x {self.stock} | {self.transaction_date} | ${self.price.c}/share | value: ${self.price.c * self.shares}]"



class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)
    cash_balance = models.DecimalField(max_digits=15, decimal_places=2, default=10000)  # Default cash balance, e.g., $10,000


    def get_aggregate_data(self):
        # Initialize a dictionary to hold aggregate data for each stock
        aggregate_data = {}

        # Loop through each order in the portfolio
        for order in self.orders.all():
            # If this is the first order for this stock, initialize data structure
            if order.stock not in aggregate_data:
                aggregate_data[order.stock] = {'total_shares': 0, 'total_spent': 0, 'average_price': None}

            # Calculate total shares and total spent based on order type
            if order.order_type == 'B':  # Buy order
                aggregate_data[order.stock]['total_shares'] += order.shares
                aggregate_data[order.stock]['total_spent'] += order.shares * order.price.c
            elif order.order_type == 'S':  # Sell order
                aggregate_data[order.stock]['total_shares'] -= order.shares
                aggregate_data[order.stock]['total_spent'] -= order.shares * order.price.c

            # Calculate the new average price
            if aggregate_data[order.stock]['total_shares'] > 0:
                aggregate_data[order.stock]['average_price'] = aggregate_data[order.stock]['total_spent'] / aggregate_data[order.stock]['total_shares']
            else:
                #remove empty holdings
                del aggregate_data[order.stock]


        return aggregate_data
    
    def update_cash_balance(self):
        # Start with the initial cash balance (e.g., $10,000)
        new_cash_balance = 10000

        # Iterate through all orders and adjust cash balance accordingly
        for order in self.orders.all().order_by('transaction_date'):
            if order.order_type == 'B':  # Buying decreases cash balance
                new_cash_balance -= order.shares * order.price.c
            elif order.order_type == 'S':  # Selling increases cash balance
                new_cash_balance += order.shares * order.price.c

        # Set the new cash balance and save
        self.cash_balance = new_cash_balance
        self.save()


    def get_portfolio_value(self, date):
        total_value = 0
        stock_shares = {}  # To hold the total shares of each stock
        initial_cash_balance = 10000
        cash = initial_cash_balance

        # Loop through orders and calculate the shares held for each stock
        for order in self.orders.filter(transaction_date__lte=date).order_by('transaction_date'):
            if order.order_type == 'B':
                stock_shares[order.stock] = stock_shares.get(order.stock, 0) + order.shares
                cash -= order.shares * order.price.c

            elif order.order_type == 'S':
                stock_shares[order.stock] = stock_shares.get(order.stock, 0) - order.shares
                cash += order.shares * order.price.c

        # Calculate the total value of the portfolio
        for stock, shares in stock_shares.items():
            if shares > 0:  # If there are shares held for this stock
                # Get the latest available price up to the given date
                latest_price = Price.objects.filter(stock=stock, date__lte=date).order_by('-date').first()
                if latest_price:
                    total_value += shares * latest_price.c  # Assuming 'c' is the closing price

        return total_value+cash



    def __str__(self):
        return f"{self.user.username}'s Portfolio"



@receiver(post_save, sender=User)
def create_user_portfolio(sender, instance, created, **kwargs):
    if created:
        Portfolio.objects.create(user=instance)

post_save.connect(create_user_portfolio, sender=User)