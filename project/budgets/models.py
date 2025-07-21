from django.db import models
from django.conf import settings
from transactions.models import Transaction
from django.utils import timezone

def get_current_month():
    today = timezone.now()
    return today.replace(day=1)

class Budget(models.Model):
    class Meta:
        unique_together = ('user', 'category', 'month')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=Transaction.ExpenseCategory.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField(default=get_current_month)

    def __str__(self):
        return f"{self.user} - {self.category} - {self.month.strftime('%B %Y')}"

    def spent(self):
        return Transaction.objects.filter(
            user=self.user,
            transaction_type='expense',
            category=self.category,
            created_at__year=self.month.year,
            created_at__month=self.month.month
        ).aggregate(models.Sum('amount'))['amount__sum'] or 0

    @property
    def remaining(self):
        return self.amount - self.spent()
