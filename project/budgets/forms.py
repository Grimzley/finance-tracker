from django import forms
from django.forms import modelformset_factory
from .models import Budget

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'limit']
        widgets = {
            'category': forms.HiddenInput(),
            'limit': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': '0.01'}),
        }

BudgetFormSet = modelformset_factory(
    Budget,
    form=BudgetForm,
    extra=0
)
