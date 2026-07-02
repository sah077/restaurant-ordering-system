"""
Django Admin configuration for the Orders app.

This is the primary interface restaurant staff will use to:
- View customer orders
- Change order status (Pending -> Preparing -> Ready -> Delivered)

As required: "Admin: Use Django Admin only" for order management.
"""

from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """
    Shows the individual food items within an order, directly on the
    Order's admin page, so staff can see exactly what was ordered
    without navigating to a separate screen.
    """
    model = OrderItem
    extra = 0
    readonly_fields = ('food_item', 'food_name', 'price', 'quantity', 'subtotal')
    can_delete = False

    def subtotal(self, obj):
        return obj.subtotal


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'full_name', 'phone_number',
        'total_price', 'status', 'created_at'
    )
    list_filter = ('status', 'created_at')
    list_editable = ('status',)  # Staff can change status right from the order list
    search_fields = ('user__username', 'full_name', 'phone_number')
    readonly_fields = (
        'user', 'full_name', 'phone_number', 'delivery_address',
        'subtotal', 'delivery_fee', 'total_price', 'created_at', 'updated_at'
    )
    inlines = [OrderItemInline]

    fieldsets = (
        ('Customer Info', {
            'fields': ('user', 'full_name', 'phone_number', 'delivery_address')
        }),
        ('Order Status', {
            'fields': ('status',)
        }),
        ('Pricing', {
            'fields': ('subtotal', 'delivery_fee', 'total_price')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def has_add_permission(self, request):
        # Orders should only be created through the checkout process on the site,
        # not manually created from the Django Admin.
        return False