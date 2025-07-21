from django.urls import path
from . import views

urlpatterns = [
    path('transactions/', views.transaction_list_view, name='transaction_list'),
    path('transactions/add/', views.create_transaction_view, name='create_transaction'),
    path('transactions/<int:pk>/edit/', views.edit_transaction_view, name='edit_transaction'),
    path('transactions/<int:pk>/delete/', views.delete_transaction_view, name='delete_transaction'),
]
