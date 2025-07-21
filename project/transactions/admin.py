from django.contrib import admin
from .models import Transaction
from .form import TransactionAdminForm

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    form = TransactionAdminForm

    list_display = ('user', 'title', 'amount', 'transaction_type', 'get_category', 'created_at')
    list_filter = ('transaction_type', 'category', 'created_at')
    search_fields = ('title', 'user__username', 'category')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    def get_category(self, obj):
        return obj.get_category()
    get_category.short_description = 'Category'
