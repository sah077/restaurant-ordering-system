"""
Models for the Menu app.

This file defines the database structure for:
- Category (e.g., Appetizers, Main Course, Desserts, Beverages)
- FoodItem (individual food items belonging to a category)
"""

from django.db import models
from django.urls import reverse


class Category(models.Model):
    """
    Represents a food category, e.g. 'Appetizers', 'Main Course', 'Desserts'.
    Categories are managed entirely through the Django Admin.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, help_text="Used in URLs, e.g. 'main-course'")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class FoodItem(models.Model):
    """
    Represents a single food item on the menu.
    Example: Margherita Pizza, Chicken Momo, Chocolate Cake.
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='food_items'
    )
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, help_text="Used in URLs")
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, help_text="Price in NPR")
    image = models.ImageField(upload_to='food_items/', blank=True, null=True)
    is_available = models.BooleanField(default=True, help_text="Uncheck to hide this item from the menu")
    is_featured = models.BooleanField(default=False, help_text="Show this item on the homepage")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the URL to view this food item's detail page."""
        return reverse('food_detail', kwargs={'slug': self.slug})