"""
Views for the Menu app.

Handles: Home page, Menu browsing, Search, Filter by category,
Food item details, About page, and Contact page.
"""

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Category, FoodItem


def home(request):
    """
    Home page view.
    Shows a hero banner and a selection of featured food items.
    """
    featured_items = FoodItem.objects.filter(is_available=True, is_featured=True)[:6]
    categories = Category.objects.all()[:6]

    context = {
        'featured_items': featured_items,
        'categories': categories,
    }
    return render(request, 'menu/home.html', context)


def menu_list(request):
    """
    Menu browsing page.
    Supports:
    - Searching by food name (?q=pizza)
    - Filtering by category (?category=main-course)
    """
    items = FoodItem.objects.filter(is_available=True)
    categories = Category.objects.all()

    # Search functionality
    query = request.GET.get('q')
    if query:
        items = items.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    # Filter by category
    selected_category = request.GET.get('category')
    if selected_category:
        items = items.filter(category__slug=selected_category)

    context = {
        'items': items,
        'categories': categories,
        'query': query or '',
        'selected_category': selected_category or '',
    }
    return render(request, 'menu/menu_list.html', context)


def food_detail(request, slug):
    """
    Food item detail page.
    Shows full description, price, image, and an Add to Cart button.
    """
    item = get_object_or_404(FoodItem, slug=slug, is_available=True)
    # Show a few related items from the same category
    related_items = FoodItem.objects.filter(
        category=item.category, is_available=True
    ).exclude(id=item.id)[:4]

    context = {
        'item': item,
        'related_items': related_items,
    }
    return render(request, 'menu/food_detail.html', context)


def about(request):
    """Static About page."""
    return render(request, 'menu/about.html')


def contact(request):
    """Static Contact page."""
    return render(request, 'menu/contact.html')