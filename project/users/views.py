from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.cache import never_cache
from datetime import date, timedelta

from .forms import RegisterForm
from transactions.forms import TransactionForm
from budgets.forms import BudgetFormSet
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth.models import User
from transactions.models import Transaction
from budgets.models import Budget

from budgets.utils import get_monthly_budget_summary
from reports.utils import get_monthly_summary, get_total_summary

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
    return render(request, 'landing.html', {'register_error': error_message, 'login_error': None, 'form': form})

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
    return render(request, 'landing.html', {'register_error': None, 'login_error': error_message, 'form': form})

def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect('dashboard')

@never_cache
@login_required
def dashboard_view(request):
    recent = Transaction.objects.filter(user=request.user).order_by('-created_at')[:7]
    form = TransactionForm()
    budgets = get_monthly_budget_summary(request.user)
    formset = BudgetFormSet(queryset=Budget.objects.filter(user=request.user))

    today = date.today()
    total = get_total_summary(request.user)
    past = []
    for i in range(5):
        first_day = (today.replace(day=1) - timedelta(days=30*i)).replace(day=1)
        summary = get_monthly_summary(request.user, first_day)
        past.append(summary)
    summary = past.pop(0)
    
    return render(request, 'dashboard.html', {'recent': recent, 'form': form, 'budgets': budgets, 'formset': formset, 'summary': summary, 'total': total, 'past': past})

@never_cache
@login_required
def settings_view(request):
    user = request.user
    password_form = PasswordChangeForm(user=user)
    password_form.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Old Password'})
    password_form.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'New Password'})
    password_form.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm New Password'})
    return render(request, 'settings.html', {'current_username': user.username, 'password_form': password_form, 'username_message': None, 'password_message': None})

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
    return render(request, 'settings.html', {'current_username': user.username, 'password_form': password_form, 'username_message': message, 'password_message': None})

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
    return render(request, 'settings.html', {'current_username': user.username, 'password_form': password_form, 'username_message': None, 'password_message': message})

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
