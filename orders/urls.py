"""
URL patterns for the Orders app.
These are included under the 'orders/' prefix in the main urls.py.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('buy-now/<int:item_id>/', views.buy_now, name='buy_now'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/<int:order_id>/', views.order_success, name='order_success'),
    path('history/', views.order_history, name='order_history'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
]