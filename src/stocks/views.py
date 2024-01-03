from django.shortcuts import render, redirect, get_object_or_404
from .models import Portfolio, Stock, Position
from django.contrib.auth.decorators import login_required
from .forms import PositionForm
from django.http import HttpResponseRedirect


'''
def stock_detail(request, symbol):
    stock = get_object_or_404(Stock, symbol=symbol.upper())
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            new_position = form.save(commit=False)
            new_position.stock = stock  # Set the stock to current stock
            new_position.save()
            request.user.portfolio.positions.add(new_position)
            return redirect('stocks:portfolio')
    else:
        form = PositionForm(initial={'symbol': stock.symbol})
    return render(request, 'stocks/stock_detail.html', {'stock': stock, 'form': form})
'''

def stock_detail(request, symbol):
    stock = get_object_or_404(Stock, symbol=symbol.upper())
    
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            new_position = form.save(commit=False)
            new_position.stock = stock  # Set the stock to the current stock
            new_position.save()
            request.user.portfolio.positions.add(new_position)
            return redirect('stocks:portfolio')
        else:
            # Provide the form with the error messages to display
            return render(request, 'stocks/stock_detail.html', {'stock': stock, 'form': form, 'error_message': 'Invalid form data. Please check the entered values.'})
    else:
        form = PositionForm(initial={'symbol': stock.symbol})
    
    return render(request, 'stocks/stock_detail.html', {'stock': stock, 'form': form})


@login_required
def portfolio(request):
    user_portfolio = get_object_or_404(Portfolio, user=request.user)
    positions = user_portfolio.positions.all()

    if request.method == 'POST':
        if 'add' in request.POST:
            form = PositionForm(request.POST)
            if form.is_valid():
                new_position = form.save(commit=False)
                new_position.stock = form.cleaned_data['symbol']  # Get the validated stock object
                new_position.save()
                user_portfolio.positions.add(new_position)
                return redirect('stocks:portfolio')  # Redirect to the portfolio page
        elif 'remove' in request.POST:
            position_id = request.POST.get('position_id')
            position = get_object_or_404(Position, id=position_id)
            user_portfolio.positions.remove(position)
            position.delete()
        return HttpResponseRedirect(request.path_info)  # Refresh the page to show changes

    else:
        form = PositionForm()
    return render(request, 'stocks/portfolio.html', {'positions': positions, 'form': form})
