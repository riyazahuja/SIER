from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Stock)
admin.site.register(Price)
admin.site.register(Order)
admin.site.register(Portfolio)