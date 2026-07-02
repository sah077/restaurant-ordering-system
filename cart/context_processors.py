"""
Context processor that makes the cart item count available in every template
(used in the navbar badge in base.html).

This runs on every request. For performance, it only queries the database
if the user is actually logged in (guests always see 0).
"""

from .models import Cart


def cart_item_count(request):
    """
    Returns the total number of items in the logged-in user's cart.
    Returns 0 for anonymous (not logged-in) users.
    """
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            return {'cart_item_count': cart.total_items}
    return {'cart_item_count': 0}