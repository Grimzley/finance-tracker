from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name="dashboard"),
    path('register/', views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('settings/', views.settings_view, name="settings"),
    path('settings/edit_username/', views.change_username_view, name="change_username"),
    path('settings/edit_password/', views.change_password_view, name="change_password"),
    path('settings/delete_user/', views.delete_user_view, name="delete_user"),
]
