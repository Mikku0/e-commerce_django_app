from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

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