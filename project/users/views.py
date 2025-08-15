from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.cache import never_cache
from datetime import date, timedelta
import json

from .forms import RegisterForm
from transactions.forms import TransactionForm
from budgets.forms import BudgetFormSet
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth.models import User
from transactions.models import Transaction
from budgets.models import Budget

from budgets.utils import get_monthly_budget_summary
from reports.utils import get_monthly_summary

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
            error_message = form
    form = RegisterForm()
    context = {
        'register_error': error_message,
        'login_error': None,
        'form': form
    }
    return render(request, 'landing.html', context)

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
            error_message = "Incorrect username/password"
    form = RegisterForm()
    context = {
        'register_error': None,
        'login_error': error_message,
        'form': form
    }
    return render(request, 'landing.html', context)

def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect('dashboard')

@never_cache
@login_required
def dashboard_view(request):
    today = date.today()
    last_month_date = (today.replace(day=1) - timedelta(days=30)).replace(day=1)
    join_date = request.user.date_joined.date()
    form = TransactionForm()
    formset = BudgetFormSet(queryset=Budget.objects.filter(user=request.user))

    # Recent Transactions
    recent = Transaction.objects.filter(user=request.user).order_by('-created_at')[:10]

    # Budget Data
    budgets = get_monthly_budget_summary(request.user)
    budgets_last_month = get_monthly_budget_summary(request.user, last_month_date)

    # Get All Monthly Reports
    month_data = []
    num_months = (today.year - join_date.year) * 12 + (today.month - join_date.month)
    if today.day < join_date.day:
        num_months -= 1
    for i in range(max(5, num_months)):
        first_day = (today.replace(day=1) - timedelta(days=30*i)).replace(day=1)
        summary = get_monthly_summary(request.user, first_day)
        month_data.append(summary)
    
    # Pie and Radar Chart Data
    budget_labels = ["Food", "Bills", "Transportation", "Shopping", "Entertainment", "Healthcare", "Savings", "Other"]
    this_month_progress = []
    this_month_spent = []
    last_month_progress = []
    for budget in budgets:
        this_month_progress.append(float(budget['progress']))
        this_month_spent.append(float(budget['spent']))
    for budget in budgets_last_month:
        last_month_progress.append(float(budget['progress']))

    # Line and Bar Chart Data
    months = []
    income = []
    savings = []
    expenses = []
    past = month_data[:5]
    for month in past:
        months.append(month['month'].strftime('%b'))
        income.append(float(month['total_income']))
        savings.append(float(month['total_savings']))
        expenses.append(float(month['total_expenses']))
    net_balance = []
    for month in month_data:
        bal = float(month['net_balance'])
        for i in range(len(net_balance)):
            net_balance[i] = net_balance[i] + bal
        net_balance.append(bal)
    summary = past[0]
    balance = net_balance[0]
    net_balance = net_balance[:5]

    context = {
        'recent': recent,
        'form': form,
        'budgets': budgets,
        'formset': formset,
        'summary': summary,
        'past': past,
        'budget_labels': json.dumps(budget_labels),
        'this_month_data': this_month_progress,
        'last_month_data': last_month_progress,
        'this_month_spent': this_month_spent,
        'months': json.dumps(months),
        'income': income,
        'savings': savings,
        'expenses': expenses,
        'net_balance': net_balance,
        'balance': balance
    }
    return render(request, 'dashboard.html', context)

@never_cache
@login_required
def settings_view(request):
    user = request.user
    password_form = PasswordChangeForm(user=user)
    password_form.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Old Password'})
    password_form.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'New Password'})
    password_form.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm New Password'})
    context = {
        'current_username': user.username,
        'password_form': password_form,
        'username_message': None,
        'password_message': None
    }
    return render(request, 'settings.html', context)

@never_cache
@login_required
def change_username_view(request):
    user = request.user
    password_form = PasswordChangeForm(user=user)
    message = None
    if request.method == 'POST':
        new_username = request.POST.get('username', '').strip()
        if not new_username:
            message = "Username cannot be empty."
        elif User.objects.filter(username=new_username).exclude(pk=user.pk).exists():
            message = "This username is already taken."
        else:
            user.username = new_username
            user.save()
            return redirect('dashboard')
    password_form.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Old Password'})
    password_form.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'New Password'})
    password_form.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm New Password'})
    context = {
        'current_username': user.username,
        'password_form': password_form,
        'username_message': message, 
        'password_message': None
    }
    return render(request, 'settings.html', context)

@never_cache
@login_required
def change_password_view(request):
    user = request.user
    password_form = PasswordChangeForm(user=user)
    message = None
    if request.method == 'POST':
        password_form = PasswordChangeForm(user=user, data=request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            return redirect('dashboard')
        else:
            message = "Incorrect password."
    password_form.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Old Password'})
    password_form.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'New Password'})
    password_form.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm New Password'})
    context = {
        'current_username': user.username,
        'password_form': password_form,
        'username_message': None,
        'password_message': message
    }
    return render(request, 'settings.html', context)

@never_cache
@login_required
def delete_user_view(request):
    if request.method == 'POST':
        user = request.user
        user.is_active = False
        user.save()
        logout(request)
        return redirect('dashboard')
    return redirect('settings')
