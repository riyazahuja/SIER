from django import forms
from .models import Position, Stock

class PositionForm(forms.ModelForm):
    symbol = forms.CharField(max_length=10, required=True, help_text="Enter the stock ticker")
    shares = forms.IntegerField(required=True)
    purchase_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Position
        fields = ['symbol', 'shares', 'purchase_date']  # Define fields in the order you want them to appear

    def clean_symbol(self):
        symbol = self.cleaned_data.get('symbol').upper()
        try:
            stock = Stock.objects.get(symbol=symbol)
        except Stock.DoesNotExist:
            raise forms.ValidationError(f"No stock found with symbol: {symbol}")
        return stock
