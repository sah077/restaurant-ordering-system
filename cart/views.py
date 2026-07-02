"""
Views for the Cart app.

Handles: Add to Cart, Update Quantity, Remove Item, View Cart.
All views require the user to be logged in, since each cart belongs to a user.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from menu.models import FoodItem
from .models import Cart, CartItem


@login_required
def cart_detail(request):
    """
    Displays the current user's cart with all items, quantities, and total price.
    """
    cart, created = Cart.objects.get_or_create(user=request.user)
    context = {
        'cart': cart,
        'cart_items': cart.items.select_related('food_item').all(),
    }
    return render(request, 'cart/cart_detail.html', context)


@login_required
@require_POST
def add_to_cart(request, item_id):
    """
    Adds a food item to the user's cart.
    If the item is already in the cart, increases its quantity instead
    of creating a duplicate row.
    Reads 'quantity' from POST data if provided (used on the Food Detail page),
    otherwise defaults to 1 (used on Home/Menu page quick-add buttons).
    """
    food_item = get_object_or_404(FoodItem, id=item_id, is_available=True)
    cart, created = Cart.objects.get_or_create(user=request.user)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        quantity = 1
    if quantity < 1:
        quantity = 1

    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        food_item=food_item,
        defaults={'quantity': quantity}
    )

    if not item_created:
        # Item was already in the cart, so add to the existing quantity
        cart_item.quantity += quantity
        cart_item.save()

    messages.success(request, f"{food_item.name} added to your cart.")

    # Redirect back to whichever page the user came from (food detail, menu, or home)
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'menu_list'
    return redirect(next_url)


@login_required
@require_POST
def update_cart_item(request, item_id):
    """
    Updates the quantity of a specific item already in the cart.
    If the submitted quantity is 0 or less, the item is removed instead.
    """
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        quantity = 1

    if quantity <= 0:
        cart_item.delete()
        messages.info(request, f"{cart_item.food_item.name} removed from your cart.")
    else:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, "Cart updated.")

    return redirect('cart_detail')


@login_required
@require_POST
def remove_from_cart(request, item_id):
    """
    Removes a specific item from the user's cart entirely.
    """
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item_name = cart_item.food_item.name
    cart_item.delete()
    messages.info(request, f"{item_name} removed from your cart.")
    return redirect('cart_detail')