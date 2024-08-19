from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Order, Category, Item, Wishlist, WishlistItem
from .forms import CustomUserCreationForm


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
    form = CustomUserCreationForm
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
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

def contact(request):
    return render(request, 'base/contact.html')

def shop_single(request):
    return render(request, 'base/shop-single.html')

def cart(request):
    return render(request, 'base/cart.html')

def checkout(request):
    return render(request, 'base/checkout.html')

def shop(request):
    return render(request, 'base/shop.html')

def thank_you(request):
    return render(request, 'base/thank-you.html')