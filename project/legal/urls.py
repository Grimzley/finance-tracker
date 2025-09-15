from django.urls import path
from . import views

urlpatterns = [
    path('legal/terms', views.terms_view, name="terms"),
    path('legal/privacy', views.privacy_view, name="privacy"),
]
