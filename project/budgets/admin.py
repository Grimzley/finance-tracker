from django.contrib import admin
from .models import Budget

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'month', 'category', 'amount', 'spent_display', 'remaining_display')
    list_filter = ('month', 'category')
    search_fields = ('user__username', 'category')
    ordering = ('-month', 'user')

    def spent_display(self, obj):
        return f"${obj.spent():.2f}"
    spent_display.short_description = 'Spent'

    def remaining_display(self, obj):
        remaining = obj.amount - obj.spent()
        return f"${remaining:.2f}"
    remaining_display.short_description = 'Remaining'
