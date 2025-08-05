from django import forms
from django.forms import modelformset_factory
from .models import Budget
from decimal import Decimal, ROUND_HALF_UP

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'limit']
        widgets = {
            'category': forms.HiddenInput(),
            'limit': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0, 
                'max': 1000000,
                'oninput': 'validateDecimalPlaces(this)'
            }),
        }

    def clean_limit(self):
        limit = self.cleaned_data['limit']
        rounded_limit = limit.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return rounded_limit

BudgetFormSet = modelformset_factory(
    Budget,
    form=BudgetForm,
    extra=0
)
