from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def home(request):
    return HttpResponse('Home page')

def dept(request):
    return render(request, 'base/thankyou.html')