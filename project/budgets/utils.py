from django.utils import timezone
from django.db.models import Sum
from transactions.models import Transaction
from budgets.models import Budget

def get_monthly_budget_summary(user, date=timezone.now()):
    spent_per_category = (
        Transaction.objects
        .filter(user=user, transaction_type='expense', created_at__year=date.year, created_at__month=date.month)
        .values('category')
        .annotate(total_spent=Sum('amount'))
    )
    spent_map = {entry['category']: entry['total_spent'] for entry in spent_per_category}
    summary = []
    for budget in Budget.objects.filter(user=user).order_by('id'):
        spent = spent_map.get(budget.category, 0)
        remaining = budget.limit - spent if budget.limit > 0 else None
        if budget.limit == 0:
            progress = 0
        else:
            progress = min(100, (spent / budget.limit) * 100)
        summary.append({
            'category': budget.category,
            'limit': budget.limit,
            'spent': spent,
            'remaining': remaining,
            'progress': progress
        })
    return summary
