"""
Main URL configuration for restaurant_system project.

This file routes URLs to the appropriate app.
Each app (accounts, menu, cart, orders) has its own urls.py file,
and we "include" them here to keep things organized.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

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
# Note: In a large-scale production setup, media would typically be served by
# nginx or cloud storage (S3, Cloudinary) instead of Django directly. For this
# project's setup (single Docker container, no separate web server), we serve
# media through Django regardless of DEBUG so uploaded images keep working.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')