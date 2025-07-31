
from django.contrib import admin
from .models import Budget

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'limit')
    list_filter = ('category',)
    search_fields = ('user__username', 'category')
