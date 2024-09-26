from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Order, Category, Item, Wishlist, WishlistItem, OrderItem
from .forms import UserForm, UserAddressForm
from django.contrib.auth import update_session_auth_hash


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
    return render(request, 'base/index.html')


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
    user_order = Order.objects.filter(user=request.user).first()
    if user_order:
        order_items = user_order.items.all()
        for order_item in order_items:
            order_item.total_price = order_item.quantity * order_item.item.price
    else:
        order_items = []

    context = {'order_items': order_items}
    return render(request, 'base/cart.html', context)


def checkout(request):
    return render(request, 'base/checkout.html')


def shop(request):
    items = Item.objects.all()
    context = {'items': items}
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
