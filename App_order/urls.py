from django.urls import path
from . import views
app_name = 'App_order'

urlpatterns = [
    path('add_to_cart/<pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('remove/<pk>/', views.remove_from_cart, name='remove'),
    path('increase_cart/<pk>/', views.increase_cart, name='increase_cart'),
    path('decrease_cart/<pk>/', views.decrease_cart, name='decrease_cart'),
]