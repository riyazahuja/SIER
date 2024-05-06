from django.contrib import admin
from django.urls import include, path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace = 'accounts')),  
    path('stocks/', include('stocks.urls', namespace='stocks')),
    path('user_home/', views.user_home, name='user_home'),  # User Home page
]
