from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import Budget
from .forms import BudgetFormSet

@login_required
def edit_budgets_view(request):
    budgets = Budget.objects.filter(user=request.user)
    if request.method == 'POST':
        formset = BudgetFormSet(request.POST, queryset=budgets)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.user = request.user
                instance.save()
        else:
            print("Formset is not valid")
            print(formset.errors)
            print(formset.non_form_errors())
    return redirect('dashboard')
