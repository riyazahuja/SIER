from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.symbol} - {self.name}"



class Position(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    shares = models.IntegerField()
    purchase_date = models.DateField()

    def __str__(self):
        return f"{self.shares} shares of {self.stock}"

class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    positions = models.ManyToManyField(Position)

    def __str__(self):
        return f"{self.user.username}'s Portfolio"



@receiver(post_save, sender=User)
def create_user_portfolio(sender, instance, created, **kwargs):
    if created:
        Portfolio.objects.create(user=instance)

post_save.connect(create_user_portfolio, sender=User)