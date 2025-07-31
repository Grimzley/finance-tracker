from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm
from transactions.forms import TransactionForm
from budgets.forms import BudgetFormSet

from django.contrib.auth.models import User
from transactions.models import Transaction
from budgets.models import Budget

from budgets.utils import get_monthly_budget_summary

def register_view(request):
    error_message = None
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            for category, _ in Transaction.ExpenseCategory.choices:
                Budget.objects.create(user=user, category=category, limit=0)
            return redirect('dashboard')
        else:
            error_message = "Invalid Credentials!"
    form = RegisterForm()
    return render(request, 'landing.html', {'error': error_message, 'form': form})

def login_view(request):
    error_message = None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'dashboard'
            return redirect(next_url)
        else:
            error_message = "Invalid Credentials!"
    form = RegisterForm()
    return render(request, 'landing.html', {'error': error_message, 'form': form})

def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect('dashboard')

@login_required
def dashboard_view(request):
    recent = Transaction.objects.filter(user=request.user).order_by('-created_at')[:7]
    form = TransactionForm()
    budgets = get_monthly_budget_summary(request.user)
    formset = BudgetFormSet(queryset=Budget.objects.filter(user=request.user))
    return render(request, 'dashboard.html', {'recent': recent, 'form': form, 'budgets': budgets, 'formset': formset})

@login_required
def settings_view(request):
    return render(request, 'settings.html')
    