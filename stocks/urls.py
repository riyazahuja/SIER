from django.urls import include, path
from . import views

app_name = 'stocks'

urlpatterns = [
    path('portfolio/', views.portfolio, name='portfolio'),
    path('<str:symbol>/', views.stock_detail, name='stock_detail')
]
