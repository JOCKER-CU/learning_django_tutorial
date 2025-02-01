from django.contrib import admin
from .models import Cart, CartItem

# class Cart(admin.Model):
#     list_display = ()

# class CartItem(admin.Model):
#     list_display = ()
# Register the Cart model
admin.site.register(Cart)

# Register the CartItem model
admin.site.register(CartItem)