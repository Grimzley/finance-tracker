from transactions.models import Transaction
from django.db.models import Sum

def get_monthly_summary(user, month):
    income = Transaction.objects.filter(
        user=user,
        transaction_type='income',
        created_at__year=month.year,
        created_at__month=month.month
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    expenses = Transaction.objects.filter(
        user=user,
        transaction_type='expense',
        created_at__year=month.year,
        created_at__month=month.month
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    return {
        'month': month,
        'total_income': income,
        'total_expenses': expenses,
        'net_savings': income - expenses
    }
