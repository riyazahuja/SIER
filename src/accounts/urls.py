# accounts/urls.py
from django.urls import path
from . import views
#from .views import CustomLogoutView
from django.contrib.auth.views import LogoutView

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', LogoutView.as_view(next_page = '/'), name='logout')
]
