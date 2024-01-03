'''
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # redirect to a success page.
            return redirect('stocks:index')  # Change to your desired redirect
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})




from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # login the user
            user = form.get_user()
            auth_login(request, user)
            return redirect('stocks:index')  # or your own route
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

'''

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy


# Registration View
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Use the aliased auth_login here
            # redirect to user home page after successful registration.
            return redirect('user_home')  # Make sure 'user_home' is the correct name of your user home URL
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

# Login View
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # login the user
            user = form.get_user()
            auth_login(request, user)  # Use the aliased auth_login here
            return redirect('user_home')  # Make sure 'user_home' is the correct name of your user home URL
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


'''
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')  # Redirect to home page or wherever you wish

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)
'''