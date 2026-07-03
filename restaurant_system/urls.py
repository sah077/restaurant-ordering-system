"""
Main URL configuration for restaurant_system project.
This file routes URLs to the appropriate app.
Each app (accounts, menu, cart, orders) has its own urls.py file,
and we "include" them here to keep things organized.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    # Django admin site (used by restaurant staff to manage menu/orders)
    path('admin/', admin.site.urls),
    # Menu app handles Home, Menu browsing, Search, Filter, Food Details
    path('', include('menu.urls')),
    # Accounts app handles Register, Login, Logout, Profile
    path('accounts/', include('accounts.urls')),
    # Cart app handles Add to Cart, Update, Remove, View Cart
    path('cart/', include('cart.urls')),
    # Orders app handles Checkout, Order History
    path('orders/', include('orders.urls')),
]

# Serve media files (uploaded food images).
# NOTE: Django's static() helper only works when DEBUG=True (it checks this
# internally, no matter how we call it). Since this project serves media
# directly through Django (single Docker container, no separate nginx layer),
# we manually add a URL pattern using django.views.static.serve so uploaded
# images keep working even with DEBUG=False.
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')