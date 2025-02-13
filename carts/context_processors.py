
from .models import Cart, CartItem
from .views import _cart_id

# def counter(request):
#     count = 0  # Initialize count to 0
#     if 'admin' in request.path:  # Check if the request path contains 'admin'
#         return {}  # Return an empty context for admin paths
#     else:
#         try:
#             cart_id = _cart_id(request)  # Get the cart ID from the session
#             cart = Cart.objects.get(cart_id=cart_id)  # Get the cart object
#             if request.user.is_authenticated:
#                 cart_items = CartItem.objects.all().filter(user=request.user)

#             else:
#                 cart_items = CartItem.objects.all().filter(cart=cart)  # Get all cart items for the cart

#             for cart_item in cart_items:
#                 count += cart_item.quantity  # Sum up the quantities
#             return {'cart_count': count}  # Return the count in a dictionary
#         except (Cart.DoesNotExist, CartItem.DoesNotExist):  # Handle the case where the cart or cart items do not exist
#             return {'cart_count': 0}  # Return 0 if the cart or cart items don't exist

def counter(request):
    count = 0  # Initialize count to 0

    if 'admin' in request.path:  # Check if the request path contains 'admin'
        return {}  # Return an empty context for admin paths

    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user)  # Get cart items for logged-in user
        else:
            cart_id = _cart_id(request)
            cart = Cart.objects.get(cart_id=cart_id)
            cart_items = CartItem.objects.filter(cart=cart)  # Get items for guest user

        count = sum(item.quantity for item in cart_items)  # Sum up all item quantities
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        pass  # If cart doesn't exist, return count as 0

    return {'cart_count': count}
