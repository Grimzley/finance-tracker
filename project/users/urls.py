from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name="dashboard"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register_view, name="register"),
    path('settings/', views.ProtectedView.as_view(), name="settings"),
]
