from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('shop/', views.shop, name='shop'),
    path('shop-single/<str:pk>', views.shop_single, name='shop-single'),
    path('about/', views.about, name='about'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('checkout/', views.checkout, name='checkout'),
    path('contact/', views.contact, name='contact'),
    path('thank-you/', views.thank_you, name='thank-you'),
    path('cart/', views.cart, name='cart'),
    path('add-coupon-in-cart/', views.add_coupon_in_cart, name='add-coupon-in-cart'),
    path('user-page/', views.user_page, name='user-page'),
    path('user-update-address/', views.user_address_update, name='user-update-address'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('add-item/<int:item_id>/', views.add_item, name='add_item'),
    path('remove-item/<int:item_id>/', views.remove_item, name='remove_item'),
]
