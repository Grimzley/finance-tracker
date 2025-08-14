from django import forms
from .models import Transaction
from decimal import Decimal, ROUND_HALF_UP
from django.core.exceptions import ValidationError

class TransactionAdminForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'

    class Media:
        js = ('js/category.js',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        transaction_type = (
            self.data.get('transaction_type') or
            self.initial.get('transaction_type') or
            (self.instance.transaction_type if self.instance else None)
        )

        if transaction_type == Transaction.TransactionType.INCOME:
            self.fields['category'].widget = forms.Select(choices=Transaction.IncomeCategory.choices)
        elif transaction_type == Transaction.TransactionType.EXPENSE:
            self.fields['category'].widget = forms.Select(choices=Transaction.ExpenseCategory.choices)
        else:
            self.fields['category'].widget = forms.Select(choices=[])

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['title', 'amount', 'transaction_type', 'category']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Title',
                'pattern': '.*[A-Za-z].*',
                'title': "Title must contain non-whitespace characters"
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Amount',
                'min': 0,
                'max': 1000000,
                'oninput': 'validateDecimalPlaces(this)'
            }),
            'transaction_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required',
            }),
        }

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount < 0:
            raise ValidationError("Amount cannot be negative")
        elif amount > 1_000_000:
            raise ValidationError("Amount cannot be greater than $1,000,000")
        rounded_amount = amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return rounded_amount

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['category'].choices= [('', 'Select transaction type first')]
        