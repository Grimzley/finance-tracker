from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TransactionForm

from .models import Transaction

@never_cache
@login_required
def transaction_list_view(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')
    form = TransactionForm()
    return render(request, 'transaction_list.html', {'form': form, 'transactions': transactions})

@login_required
def create_transaction_view(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            next_url = request.POST.get('next', 'dashboard')
            return redirect(next_url)
    return redirect('transaction_list')

@login_required
def edit_transaction_view(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
    return redirect('transaction_list')

@login_required
def delete_transaction_view(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
    return redirect('transaction_list')
