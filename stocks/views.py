from django.shortcuts import render, redirect, get_object_or_404
from .models import Portfolio, Stock, Order, Price
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from django.http import HttpResponseRedirect
from datetime import date, timedelta
import json
from django.utils.safestring import mark_safe
from .lstm import run_prediction



def stock_detail(request, symbol):
    stock = get_object_or_404(Stock, symbol=symbol.upper())

    prices = Price.objects.filter(stock=stock).order_by('date')
    dates = [price.date.strftime("%Y-%m-%d") for price in prices]  # Format dates as strings
    closing_prices = [str(price.c) for price in prices]  # Assuming 'c' is the closing price

    dates = mark_safe(json.dumps(dates))
    closing_prices = mark_safe(json.dumps(closing_prices))

    predictions = []
    prediction_error = ''  # To handle any error with predictions

    if request.method == 'POST':
        # Handling prediction form submission
        if 'predict' in request.POST:
            start_date = request.POST.get('start_date')
            forecast_horizon = int(request.POST.get('forecast_horizon', 30))  # Default to 30 days if not provided

            # Set window size based on forecast horizon
            if forecast_horizon == 7:
                window_size = 60
            elif forecast_horizon == 90:
                window_size = 360
            else:  # Default to 30 days
                window_size = 120

            if start_date:
                try:
                    predictions = run_prediction(symbol, window_size, forecast_horizon, start_date)
                except Exception as e:
                    prediction_error = str(e)
            else:
                prediction_error = "Please provide a valid start date."

            print(f"Pred: {predictions}\n Error: {prediction_error}")
            
            start_idx = predictions['forecast_dates'].index[0]
            

            predictions['start_date'] = predictions['start_date'].strftime("%Y-%m-%d")
            predictions['predicted_prices'] = [float(p) for p in predictions['predicted_prices']]
            predictions['forecast_dates'] = [d.strftime("%Y-%m-%d") for d in predictions['forecast_dates']]
            predictions['dates_full'] = [d.strftime("%Y-%m-%d") for d in predictions['dates_full']]
            predictions['actual_prices'] = [float(p) for p in predictions['actual_prices']]
            predictions['actual_prices_full'] = [float(p) for p in predictions['actual_prices_full']]
            predictions['rmse'] = float(predictions['rmse'])
            predictions['rmspe'] = float(predictions['rmspe'])

            #padding:
            temp = [None for i in range(start_idx)]
            predictions['predicted_prices'] = temp + predictions['predicted_prices']

            
            predictions = mark_safe(json.dumps(predictions))
            #print(predictions)
            #print(prediction_error)



        form = OrderForm(request.POST)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.stock = stock  # Set the stock to the current stock
            new_order.validate_and_set_price()  # Ensure the price is valid and set

            if new_order.price:  # If a valid price was found
                new_order.save()
                request.user.portfolio.orders.add(new_order)
                request.user.portfolio.update_cash_balance()  # Update the user's cash balance
                return redirect('stocks:portfolio')
            else:
                # If no valid price found, provide an appropriate error message
                return render(request, 'stocks/stock_detail.html', {'stock': stock, 'form': form, 'dates': dates, 'closing_prices': closing_prices, 'predictions': predictions, 'error_message': 'No valid price found for the given date.'})
        else:
            # If form is not valid, render the page again with error messages
            return render(request, 'stocks/stock_detail.html', {'stock': stock, 'form': form, 'dates': dates, 'closing_prices': closing_prices, 'predictions': predictions, 'error_message': 'Invalid form data. Please check the entered values.'})
    else:
        # Pre-fill the form with the stock symbol and current date as the transaction date
        form = OrderForm(initial={'transaction_date': date.today()})
    
    return render(request, 'stocks/stock_detail.html', {'stock': stock, 'form': form, 'dates': dates, 'predictions': predictions, 'error_message': prediction_error, 'closing_prices': closing_prices})









@login_required
def portfolio(request):
    user_portfolio = get_object_or_404(Portfolio, user=request.user)
    aggregate_data = user_portfolio.get_aggregate_data()



     # Find the first order date
    first_order = user_portfolio.orders.order_by('transaction_date').first()
    if first_order:
        start_date = first_order.transaction_date - timedelta(weeks=1)  # One week before the first order
    else:
        # If there are no orders, you might start from a default date or today
        start_date = date.today() - timedelta(weeks=1)  # For example, one week ago from today

    end_date = date.today()  # Up to the present

    # Generate the range of dates (you might want to ensure there's a limit on the number of dates for performance reasons)
    dates = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

    # Calculate portfolio values for each date
    portfolio_values = [str(user_portfolio.get_portfolio_value(d)) for d in dates]

    dates = [date.strftime("%Y-%m-%d") for date in dates]

    dates = mark_safe(json.dumps(dates))
    portfolio_values = mark_safe(json.dumps(portfolio_values))



    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.stock = form.cleaned_data['ticker']  # Set the stock based on validated ticker
            new_order.validate_and_set_price()

            if new_order.price and new_order.stock:
                new_order.save()
                user_portfolio.orders.add(new_order)
                user_portfolio.update_cash_balance()
                return redirect('stocks:portfolio')
            else:
                return render(request, 'stocks/portfolio.html', {
                    'user_portfolio': user_portfolio,
                    'aggregate_data': aggregate_data,
                    'form': form,
                    'dates': dates,
                    'portfolio_values': portfolio_values,
                    'error_message' : 'No valid price found for the given date.'
                })
        else:
            return render(request, 'stocks/portfolio.html', {
                'user_portfolio': user_portfolio,
                'aggregate_data': aggregate_data,
                'form': form,
                'dates': dates,
                'portfolio_values': portfolio_values,
                'error_message' : 'Invalid form data. Please check the entered values.'
            })
    else:
        form = OrderForm()

    return render(request, 'stocks/portfolio.html', {
        'user_portfolio': user_portfolio,
        'aggregate_data': aggregate_data,
        'form': form,
        'dates': dates,
        'portfolio_values': portfolio_values
    })
