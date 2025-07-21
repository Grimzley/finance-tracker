from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from  datetime import date
from .models import Budget, Transaction
from .forms import BudgetForm

@login_required
def budget_list_view(request):
    curr_month = date.today().replace(day=1)
    budgets = Budget.objects.filter(user=request.user, month=curr_month).order_by('category')

    all_categories = [key for key, _ in Transaction.ExpenseCategory.choices]
    used_categories = budgets.values_list('category', flat=True)

    available_categories = [cat for cat in all_categories if cat not in used_categories]
    form_disabled = len(available_categories) == 0

    if request.method == 'POST' and not form_disabled:
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.month = curr_month
            budget.save()
            return redirect('budget_list')
    else:
        form = BudgetForm(user=request.user, month=curr_month) if not form_disabled else None
    return render(request, 'budget_list.html', {
        'form': form,
        'budgets': budgets,
        'curr_month': curr_month,
        'form_disabled': form_disabled
    })

@login_required
def edit_budget_view(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    curr_month = budget.month

    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget, user=request.user, month=curr_month)
        if form.is_valid():
            form.save()
            return redirect('budget_list')
    else:
        form = BudgetForm(instance=budget, user=request.user, month=curr_month)

    return render(request, 'edit_budget.html', {'form': form, 'budget': budget})

@login_required
def delete_budget_view(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        budget.delete()
    return redirect('budget_list')
