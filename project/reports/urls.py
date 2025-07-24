from django.urls import path
from . import views

urlpatterns = [
    path('reports/', views.report_list_view, name='report_list'),
]