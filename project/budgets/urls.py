from django.urls import path
from . import views

urlpatterns = [
    path('budgets/edit/', views.edit_budgets_view, name='edit_budget'),
]
