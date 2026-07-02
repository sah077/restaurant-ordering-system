"""
URL patterns for the Accounts app.

Login and Logout use Django's built-in class-based auth views —
we just point them to our own custom templates.
Register and Profile use our own custom views.
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),

    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html'
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(
        next_page='home'
    ), name='logout'),

    path('profile/', views.profile, name='profile'),
]