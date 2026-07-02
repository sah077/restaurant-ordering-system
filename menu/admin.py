"""
Django Admin configuration for the Menu app.

This makes Category and FoodItem manageable from the Django Admin panel
at /admin/. This satisfies the requirement:
"Admin: Use Django Admin only - Add/Edit/Delete categories and food items."
"""

from django.contrib import admin
from .models import Category, FoodItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}  # Auto-fills slug as you type the name
    search_fields = ('name',)


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available', 'is_featured', 'created_at')
    list_filter = ('category', 'is_available', 'is_featured')
    list_editable = ('is_available', 'is_featured')  # Quickly toggle these from the list view
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}  # Auto-fills slug as you type the name

    # Group fields nicely in the edit form
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'name', 'slug', 'description')
        }),
        ('Pricing & Image', {
            'fields': ('price', 'image')
        }),
        ('Visibility', {
            'fields': ('is_available', 'is_featured')
        }),
    )