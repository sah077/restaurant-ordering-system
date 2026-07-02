"""
URL patterns for the Menu app.
These are included at the root path ('') in the main urls.py,
so 'home' becomes '/' and 'menu_list' becomes '/menu/'.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu_list, name='menu_list'),
    path('menu/<slug:slug>/', views.food_detail, name='food_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]