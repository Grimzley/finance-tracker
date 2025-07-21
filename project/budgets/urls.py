from django.urls import path
from . import views

urlpatterns = [
    path('budgets/', views.budget_list_view, name='budget_list'),
    path('budgets/<int:pk>/edit/', views.edit_budget_view, name='edit_budget'),
    path('budgets/<int:pk>/delete/', views.delete_budget_view, name='delete_budget'),
]
