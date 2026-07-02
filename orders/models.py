"""
Models for the Orders app.

An Order is created when a user checks out their cart.
Each Order contains multiple OrderItems (a snapshot of what was purchased,
at what price, and in what quantity — kept separate from CartItem so that
future price changes to a FoodItem don't affect historical order records).
"""
"""
Models for the Orders app.
...
"""

from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from menu.models import FoodItem

DELIVERY_FEE = Decimal('50.00')  # Flat delivery fee in NPR, used when creating new orders

class Order(models.Model):
    """
    Represents a placed order. Created during checkout from the user's cart.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('delivered', 'Delivered'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('esewa', 'eSewa'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Payment details
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cod')
    is_paid = models.BooleanField(
        default=False,
        help_text="For eSewa orders: check this box once you've confirmed the payment in your eSewa app."
    )

    # Delivery details captured at checkout time
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    delivery_address = models.TextField()

    # Pricing snapshot (so historical orders stay accurate even if prices change later)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=8, decimal_places=2, default=DELIVERY_FEE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} ({self.get_status_display()})"


class OrderItem(models.Model):
    """
    Represents a single food item within a placed order.
    Stores the food item's name and price AT THE TIME OF ORDERING,
    so the order history stays accurate even if the FoodItem is later
    edited, repriced, or deleted from the menu.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.SET_NULL, null=True, blank=True)

    # Snapshot fields (kept even if the original FoodItem is deleted)
    food_name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.food_name}"

    @property
    def subtotal(self):
        """Returns price * quantity for this order line item."""
        return self.price * self.quantity