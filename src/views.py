from django.shortcuts import render

def home(request):
    return render(request, 'home.html')


from django.contrib.auth.decorators import login_required

@login_required
def user_home(request):
    context = {'username': request.user.username}
    return render(request, 'user_home.html', context)