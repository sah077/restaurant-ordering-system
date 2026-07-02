"""
Models for the Cart app.

Each logged-in user has exactly one Cart, which contains multiple CartItems.
A CartItem links a FoodItem to a quantity.
"""

from django.db import models
from django.contrib.auth.models import User
from menu.models import FoodItem


class Cart(models.Model):
    """
    Represents a shopping cart belonging to a single user.
    Each user has exactly one cart (created automatically the first time
    they add an item).
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    @property
    def total_price(self):
        """Returns the total price of all items in the cart."""
        return sum(item.subtotal for item in self.items.all())

    @property
    def total_items(self):
        """Returns the total number of individual items (sum of quantities) in the cart."""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """
    Represents a single food item and its quantity within a user's cart.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # A user shouldn't have two separate CartItem rows for the same food item
        unique_together = ('cart', 'food_item')

    def __str__(self):
        return f"{self.quantity} x {self.food_item.name}"

    @property
    def subtotal(self):
        """Returns price * quantity for this cart item."""
        return self.food_item.price * self.quantity