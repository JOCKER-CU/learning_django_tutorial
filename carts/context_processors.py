
from .models import Cart, CartItem
from .views import _cart_id

def counter(request):
    count = 0  # Initialize count to 0
    if 'admin' in request.path:  # Check if the request path contains 'admin'
        return {}  # Return an empty context for admin paths
    else:
        try:
            cart_id = _cart_id(request)  # Get the cart ID from the session
            cart = Cart.objects.get(cart_id=cart_id)  # Get the cart object
            cart_items = CartItem.objects.filter(cart=cart)  # Get all cart items for the cart
            for cart_item in cart_items:
                count += cart_item.quantity  # Sum up the quantities
            return {'cart_count': count}  # Return the count in a dictionary
        except Cart.DoesNotExist:  # Handle the case where the cart does not exist
            return {'cart_count': 0}  # Return 0 if the cart doesn't exist