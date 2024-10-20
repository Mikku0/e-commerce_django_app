from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Order, Category, Item, Wishlist, WishlistItem, OrderItem, Coupon
from .forms import UserForm, UserAddressForm
from django.contrib.auth import update_session_auth_hash
from decimal import Decimal
from .app_views.cart_views import *
from .app_views.auth_views import login_page, logout_user, register_page


def home(request):
    items = Item.objects.all()
    context = {'items': items}
    return render(request, 'base/index.html', context)


def about(request):
    return render(request, 'base/about.html')


def wishlist(request):
    user_wishlist = Wishlist.objects.filter(user=request.user).first()
    if user_wishlist:
        wishlist_items = user_wishlist.items.all()
    else:
        wishlist_items = []
    context = {
        'wishlist_items': wishlist_items
    }
    return render(request, 'base/wishlist.html', context)


def contact(request):
    return render(request, 'base/contact.html')


def shop_single(request, pk):
    item = Item.objects.get(id=pk)
    featured_items = Item.objects.all()[:6]
    context = {'item': item, 'featured_items': featured_items}
    return render(request, 'base/shop-single.html', context)


def checkout(request):
    return render(request, 'base/checkout.html')


def shop(request):
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    size = request.GET.getlist('size')
    color = request.GET.get('color')

    items = Item.objects.all()

    if category:
        items = items.filter(category__name=category)

    if min_price and not max_price:
        items = items.filter(price__gte=min_price)
    elif not min_price and max_price:
        items = items.filter(price__lte=max_price)
    elif min_price and max_price:
        items = items.filter(price__gte=min_price, price__lte=max_price)

    if size:
        items = items.filter(size__in=size)

    if color:
        items = items.filter(color=color)

    context = {
        'items': items,
        'selected_category': category,
        'selected_min_price': min_price,
        'selected_max_price': max_price,
        'selected_size': size,
        'selected_color': color,
    }

    return render(request, 'base/shop.html', context)


def thank_you(request):
    return render(request, 'base/thank-you.html')


def user_page(request):
    return render(request, 'base/user-page.html')


def user_address_update(request):
    user = request.user
    username = request.user.username
    form = UserAddressForm(instance=user)

    if request.method == 'POST':
        form = UserAddressForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user)  # To prevent logout
            messages.success(request, 'Billing Address has been updated!')
            return redirect('user-page')
        else:
            request.user.username = username
            messages.error(request, 'invalid data')

    return render(request, 'base/user-update-address.html', {'form': form})
