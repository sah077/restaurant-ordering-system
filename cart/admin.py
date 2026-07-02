"""
Django Admin configuration for the Cart app.

Carts aren't a primary admin-managed feature (they're managed by users
through the site), but we register them so staff can inspect carts for
debugging/support purposes if needed.
"""

from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    """Allows viewing/editing CartItems directly within the Cart admin page."""
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_items', 'total_price', 'updated_at')
    inlines = [CartItemInline]
    search_fields = ('user__username',)