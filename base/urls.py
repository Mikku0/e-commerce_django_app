from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),    
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('shop/', views.shop, name='shop'),
    path('shop-single/', views.shop_single, name='shop-single'),
    path('about/', views.about, name='about'),
    path('checkout/', views.checkout, name='checkout'),
    path('contact/', views.contact, name='contact'),
    path('thank-you/', views.thank_you, name='thank-you'),
    path('cart/', views.cart, name='cart'), 
]
