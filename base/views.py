from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Order, Category, Item, Wishlist, WishlistItem, OrderItem
from .forms import UserForm, UserAddressForm
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from decimal import Decimal


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


@login_required(login_url='login')
def cart(request):

    COUPONS = {
        'discount10': 10,
        'discount20': 20
    }
    coupon_discount = 0
    coupon = ''
    discount_value = 0
    invalid_coupon = False
    original_value = 0

    user_order = Order.objects.filter(user=request.user).first()
    if user_order:
        order_items = user_order.items.all()
        user_order.total_price = 0
        for order_item in order_items:
            order_item.total_price = order_item.quantity * order_item.item.price
            user_order.total_price += order_item.total_price
        original_value = user_order.total_price
    else:
        order_items = []
    if 'coupon_code' in request.POST:  # to external method before commit
        coupon_code = request.POST.get('coupon_code', '').strip()
        if coupon_code in COUPONS:
            coupon = coupon_code
            coupon_discount = COUPONS[coupon_code]
            discount_value = user_order.total_price*(Decimal(coupon_discount) / Decimal(100))
            user_order.total_price -= discount_value
            user_order.total_price = round(user_order.total_price, 2)
            messages.success(request, f'Coupon "{coupon_code}" applied successfully for {coupon_discount}% discount!')
        else:
            invalid_coupon = True

    user_order.save()

    context = {
        'order_items': order_items,
        'final_price': user_order.total_price,
        'coupon_value': coupon_discount,
        'invalid_coupon': invalid_coupon,
        'discount_value': round(discount_value, 2),
        'original_value': original_value,
        'coupon': coupon

    }
    return render(request, 'base/cart.html', context)


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


@login_required(login_url='login')
def update_quantity(request, order_item_id, action):
    order_item = get_object_or_404(OrderItem, id=order_item_id, order__user=request.user)

    if action == 'increase':
        order_item.quantity += 1
    elif action == 'decrease' and order_item.quantity > 1:
        order_item.quantity -= 1

    order_item.save()
    return redirect('cart')


@login_required(login_url='login')
def remove_item(request, order_item_id):
    order_item = get_object_or_404(OrderItem, id=order_item_id, order__user=request.user)
    order_item.delete()
    return redirect('cart')


@login_required(login_url='login')
def update_cart(request):
    if request.method == 'POST':
        user_order = Order.objects.filter(user=request.user).first()
        if user_order:
            if 'remove_item' in request.POST:
                order_item_id = request.POST.get('remove_item')
                order_item = user_order.items.filter(id=order_item_id).first()
                if order_item:
                    order_item.delete()
            else:
                for order_item in user_order.items.all():
                    quantity_field = f'quantity_{order_item.id}'
                    if quantity_field in request.POST:
                        new_quantity = int(request.POST[quantity_field])
                        if new_quantity > 0:
                            order_item.quantity = new_quantity
                            order_item.save()

        return redirect('cart')


@login_required(login_url='login')
def add_item_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    order, created = Order.objects.get_or_create(user=request.user, status='pending')

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        order_item, order_item_created = OrderItem.objects.get_or_create(order=order, item=item)

        if not order_item_created:
            order_item.quantity += quantity
        else:
            order_item.quantity = quantity

        order_item.total_price = order_item.quantity * item.price
        order_item.save()
        order.save()
        return redirect('cart')
