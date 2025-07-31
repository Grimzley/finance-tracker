from django.db import models
from django.conf import settings
from transactions.models import Transaction

class Budget(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=Transaction.ExpenseCategory.choices)
    limit = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ('user', 'category')

    def __str__(self):
        return f"{self.user} - {self.category}: ${self.limit}"
