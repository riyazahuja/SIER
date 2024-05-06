from django import forms
from .models import Order, Stock


class OrderForm(forms.ModelForm):
    ticker = forms.CharField(max_length=10, required=True, help_text="Enter the stock ticker")

    class Meta:
        model = Order
        fields = ['ticker', 'shares', 'order_type', 'transaction_date']
        widgets = {
            'transaction_date': forms.DateInput(attrs={'type': 'date'}),
        }
        # Exclude the stock field from the form itself, as it will be set based on the ticker

    def clean_ticker(self):
        ticker = self.cleaned_data['ticker'].upper()  # Normalize ticker to uppercase
        try:
            stock = Stock.objects.get(symbol=ticker)  # Attempt to find the stock
        except Stock.DoesNotExist:
            raise forms.ValidationError(f"No stock found with ticker: {ticker}")
        return stock  # Return the stock object instead of the ticker
