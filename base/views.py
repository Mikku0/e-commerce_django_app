from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Order, Category, Item, Wishlist, WishlistItem, OrderItem, Coupon
from .forms import UserForm, UserAddressForm
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from decimal import Decimal
from .app_views.cart_views import cart, update_cart, add_item_to_cart, add_coupon_in_cart, remove_item_from_cart


def login_page(request):
    page = 'login'

    if request.user.is_authenticated:
        messages.success(request, 'You are already logged in')
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email or password is wrong')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def register_page(request):
    form = UserForm

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred')

    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    items = Item.objects.all()
    context = {'items': items}
    return render(request, 'base/index.html', context)


def about(request):
    return render(request, 'base/about.html')


def wishlist(request):
    return render(request, 'base/wishlist.html')


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
