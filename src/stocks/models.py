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
    





class Position(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    shares = models.IntegerField()
    purchase_date = models.DateField()

    def __str__(self):
        return f"{self.shares} shares of {self.stock}"

class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    positions = models.ManyToManyField(Position)
    #cash_balance = models.DecimalField(max_digits=15, decimal_places=2, default=10000)  # Default cash balance, e.g., $10,000


    def __str__(self):
        return f"{self.user.username}'s Portfolio"



@receiver(post_save, sender=User)
def create_user_portfolio(sender, instance, created, **kwargs):
    if created:
        Portfolio.objects.create(user=instance)

post_save.connect(create_user_portfolio, sender=User)