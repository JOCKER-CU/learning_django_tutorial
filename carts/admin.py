from django.contrib import admin
from .models import Cart, CartItem

class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'active')
# Register the Cart model
admin.site.register(Cart, CartAdmin)

# Register the CartItem model
admin.site.register(CartItem, CartItemAdmin)