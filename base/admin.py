from django.contrib import admin
from .models import CustomUser, Order, Category, Item, Wishlist, WishlistItem, OrderItem, Coupon

admin.site.register(CustomUser)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Wishlist)
admin.site.register(WishlistItem)
admin.site.register(Coupon)
