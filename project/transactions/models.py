from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        INCOME = 'income', 'Income'
        EXPENSE = 'expense', 'Expense'

    class IncomeCategory(models.TextChoices):
        SALARY = 'salary', 'Salary'
        FREELANCE = 'freelance', 'Freelance'
        INVESTMENT = 'investment', 'Investment'
        GIFT = 'gift', 'Gift'
        OTHER = 'inc_other', 'Other'

    class ExpenseCategory(models.TextChoices):
        FOOD = 'food', 'Food'
        BILLS = 'bills', 'Bills'
        TRANSPORT = 'transport', 'Transportation'
        HEALTH = 'health', 'Healthcare'
        ENTERTAINMENT = 'entertainment', 'Entertainment'
        SHOPPING = 'shopping', 'Shopping'
        OTHER = 'exp_other', 'Other'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=7, choices=TransactionType.choices)
    category = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type}: {self.title} (${self.amount})"

    def get_category(self):
        if self.transaction_type == self.TransactionType.INCOME:
            category_dict = dict(self.IncomeCategory.choices)
        else:
            category_dict = dict(self.ExpenseCategory.choices)
        return category_dict.get(self.category, self.category)
    
    def clean(self):
        super().clean()
        valid_categories = (
            [choice[0] for choice in self.IncomeCategory.choices]
            if self.transaction_type == self.TransactionType.INCOME
            else [choice[0] for choice in self.ExpenseCategory.choices]
        )
        if self.category not in valid_categories:
            raise ValidationError(f"Category '{self.category}' is invalid for transaction type '{self.transaction_type}'")
