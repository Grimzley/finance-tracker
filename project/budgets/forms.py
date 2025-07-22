from django import forms
from .models import Budget, Transaction

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'placeholder': 'Enter your budget limit',
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        month = kwargs.pop('month', None)
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        if user and month:
            used_categories = Budget.objects.filter(
                user=user,
                month=month
            ).values_list('category', flat=True)

            if instance:
                used_categories = used_categories.exclude(pk=instance.pk)

            self.fields['category'].choices = [
                (key, label) for key, label in Transaction.ExpenseCategory.choices
                if key not in used_categories
                or (instance and key == instance.category)
            ]
    