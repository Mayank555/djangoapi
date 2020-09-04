from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('api/login/', views.LoginView, name='login'),
    path('', views.HomePage, name='home'),
]