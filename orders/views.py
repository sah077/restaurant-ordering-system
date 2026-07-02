"""
Views for the Orders app.

Handles: Checkout (converts cart into an order) and Order History.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from cart.models import Cart
from .models import Order, OrderItem, DELIVERY_FEE


@login_required
def checkout(request):
    """
    Displays the checkout form (delivery details) and, on submission,
    converts the user's cart into a permanent Order + OrderItems.
    The cart is emptied after a successful order.
    """
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('food_item').all()

    if not cart_items:
        messages.warning(request, "Your cart is empty. Add some items before checking out.")
        return redirect('menu_list')

    subtotal = cart.total_price
    total_price = subtotal + DELIVERY_FEE

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        delivery_address = request.POST.get('delivery_address', '').strip()

        # Basic server-side validation
        if not full_name or not phone_number or not delivery_address:
            messages.error(request, "Please fill in all delivery details.")
        else:
            # Use a database transaction so the Order and all OrderItems
            # are created together — if anything fails, nothing is saved.
            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    full_name=full_name,
                    phone_number=phone_number,
                    delivery_address=delivery_address,
                    subtotal=subtotal,
                    delivery_fee=DELIVERY_FEE,
                    total_price=total_price,
                )

                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        food_item=cart_item.food_item,
                        food_name=cart_item.food_item.name,
                        price=cart_item.food_item.price,
                        quantity=cart_item.quantity,
                    )

                # Empty the cart now that the order has been placed
                cart_items.delete()

            messages.success(request, f"Order #{order.id} placed successfully! Thank you for ordering.")
            return redirect('order_success', order_id=order.id)

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'delivery_fee': DELIVERY_FEE,
        'total_price': total_price,
        # Pre-fill the form with the user's existing profile info for convenience
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