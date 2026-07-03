"""
Views for the Orders app.

Handles: Checkout (converts cart OR a single "Buy Now" item into an order),
Order History, and Order Detail.
"""

import re
from types import SimpleNamespace
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db import transaction
from cart.models import Cart
from menu.models import FoodItem
from .models import Order, OrderItem, DELIVERY_FEE


@login_required
@require_POST
def buy_now(request, item_id):
    """
    Starts a 'direct order' flow for a single food item, bypassing the cart.
    Stores the item + quantity in the session, then redirects to checkout.
    This does NOT touch the user's actual Cart.
    """
    food_item = get_object_or_404(FoodItem, id=item_id, is_available=True)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        quantity = 1
    if quantity < 1:
        quantity = 1

    # Store the buy-now item in the session (temporary, per-user, not the DB cart)
    request.session['buy_now'] = {'item_id': food_item.id, 'quantity': quantity}

    return redirect('checkout')


@login_required
def checkout(request):
    """
    Displays the checkout form and, on submission, creates a permanent Order.

    Handles TWO possible sources of items:
    1. A 'Buy Now' single item stored in the session (request.session['buy_now'])
    2. The user's normal Cart (used when no buy_now session data is present)
    """
    buy_now_data = request.session.get('buy_now')

    if buy_now_data:
        # ---- Direct "Buy Now" checkout for a single item ----
        food_item = get_object_or_404(FoodItem, id=buy_now_data['item_id'], is_available=True)
        quantity = buy_now_data['quantity']

        # Build a simple stand-in object list so the template can use the
        # same {{ cart_item.food_item }} / {{ cart_item.quantity }} syntax
        # as it does for real cart items.
        cart_items = [SimpleNamespace(
            food_item=food_item,
            quantity=quantity,
            subtotal=food_item.price * quantity,
        )]
        subtotal = food_item.price * quantity
        is_buy_now = True
    else:
        # ---- Normal cart-based checkout ----
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.select_related('food_item').all()

        if not cart_items:
            messages.warning(request, "Your cart is empty. Add some items before checking out.")
            return redirect('menu_list')

        subtotal = cart.total_price
        is_buy_now = False

    total_price = subtotal + DELIVERY_FEE

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        delivery_address = request.POST.get('delivery_address', '').strip()
        payment_method = request.POST.get('payment_method', 'cod')

        phone_pattern = re.compile(r'^(98|97)\d{8}$')

        if not full_name or not phone_number or not delivery_address:
            messages.error(request, "Please fill in all delivery details.")
        elif not phone_pattern.match(phone_number):
            messages.error(request, "Please enter a valid 10-digit phone number starting with 98 or 97.")
        elif payment_method not in ('cod', 'esewa'):
            messages.error(request, "Please select a valid payment method.")
        else:
            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    full_name=full_name,
                    phone_number=phone_number,
                    delivery_address=delivery_address,
                    subtotal=subtotal,
                    delivery_fee=DELIVERY_FEE,
                    total_price=total_price,
                    payment_method=payment_method,
                )

                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        food_item=cart_item.food_item,
                        food_name=cart_item.food_item.name,
                        price=cart_item.food_item.price,
                        quantity=cart_item.quantity,
                    )

                if is_buy_now:
                    # Clear the session data — this was a one-off direct order
                    del request.session['buy_now']
                else:
                    # Empty the real cart now that the order has been placed
                    cart_items.delete()

            if payment_method == 'esewa':
                messages.success(request, f"Order #{order.id} placed! Please scan the eSewa QR code to complete payment.")
            else:
                messages.success(request, f"Order #{order.id} placed successfully! Thank you for ordering.")
            return redirect('order_success', order_id=order.id)

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'delivery_fee': DELIVERY_FEE,
        'total_price': total_price,
        'default_full_name': request.user.get_full_name() or request.user.username,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def order_success(request, order_id):
    """
    Simple confirmation page shown right after a successful order placement.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})


@login_required
def order_history(request):
    """
    Displays a list of all past orders placed by the logged-in user,
    most recent first.
    """
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    return render(request, 'orders/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    """
    Displays full details of a single past order, including all items ordered.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})