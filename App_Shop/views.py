from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Product, Category
from django.contrib.auth.mixins import LoginRequiredMixin


class Home(ListView):
    model = Product
    template_name = 'App_Shop/home.html'


class ProductDetail(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'App_Shop/product_detail.html'