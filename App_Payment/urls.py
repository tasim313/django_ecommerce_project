from django.urls import path
from . import views
app_name = 'App_Payment'

urlpatterns = [
     path('checkout/', views.checkout, name='CheckOut'),
     path('pay/', views.payment, name='payment'),
     path('status/', views.complete, name='complete'),
     path('purchase/<val_id>/<tran_id>/', views.purchase, name="purchase"),
     path('orders/', views.order_view, name="orders"),
]