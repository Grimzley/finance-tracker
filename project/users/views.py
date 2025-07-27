from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

def register_view(request):
    error_message = None
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
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
    return render(request, 'dashboard.html')

class ProtectedView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        return render(request, 'settings.html')
    