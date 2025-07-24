from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from datetime import date, timedelta
from .utils import get_monthly_summary
from transactions.models import Transaction
from django.db.models import Sum

@login_required
def report_list_view(request):
    today = date.today()
    summaries = []

    for i in range(6):  # Show last 6 months
        first_day = (today.replace(day=1) - timedelta(days=30*i)).replace(day=1)
        summary = get_monthly_summary(request.user, first_day)
        summaries.append(summary)

    return render(request, 'report_list.html', {'summaries': summaries})

@login_required
def monthly_summary(request):
    today = date.today()
    user = request.user

    transactions = Transaction.objects.filter(
        user=user,
        created_at__year=today.year,
        created_at__month=today.month
    )

    income_total = transactions.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    expense_total = transactions.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0

    category_expenses = transactions.filter(transaction_type='expense').values('category').annotate(total=Sum('amount'))

    context = {
        'income_total': income_total,
        'expense_total': expense_total,
        'category_labels': [item['category'] for item in category_expenses],
        'category_totals': [float(item['total']) for item in category_expenses],
    }
    return render(request, 'reports/monthly_summary.html', context)
