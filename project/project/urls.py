from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('slurp/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('transactions.urls')),
    path('', include('budgets.urls')),
    path('', include('reports.urls')),
]
