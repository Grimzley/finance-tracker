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
    ).exclude(category='savings').aggregate(Sum('amount'))['amount__sum'] or 0

    savings = Transaction.objects.filter(
        user=user,
        transaction_type='expense',
        category='savings',
        created_at__year=month.year,
        created_at__month=month.month
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    return {
        'month': month,
        'total_income': income,
        'total_expenses': expenses,
        'total_savings': savings,
    }

def get_total_summary(user):
    income = Transaction.objects.filter(
        user=user,
        transaction_type='income',
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    expenses = Transaction.objects.filter(
        user=user,
        transaction_type='expense',
    ).exclude(category='savings').aggregate(Sum('amount'))['amount__sum'] or 0

    savings = Transaction.objects.filter(
        user=user,
        transaction_type='expense',
        category='savings',
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    return {
        'total_income': income,
        'total_expenses': expenses,
        'total_savings': savings,
    }
