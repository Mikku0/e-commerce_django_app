from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('dept/', views.dept, name='dept')
]
