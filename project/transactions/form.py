from django import forms
from .models import Transaction

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
                'placeholder': 'Title'
            }),
            'amount': forms.NumberInput(attrs={
                'placeholder': 'Amount'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['category'].widget = forms.Select(choices=[('', 'Select transaction type first')])

        transaction_type = self.data.get('transaction_type') or self.initial.get('transaction_type')
        if transaction_type == Transaction.TransactionType.INCOME:
            self.fields['category'].choices = Transaction.IncomeCategory.choices
        elif transaction_type == Transaction.TransactionType.EXPENSE:
            self.fields['category'].choices = Transaction.ExpenseCategory.choices
