from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from .models import BillingAddress
from .forms import BillingForm
from App_order.models import Order, Cart
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
import socket
from django.views.decorators.csrf import csrf_exempt


@login_required
def checkout(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    form = BillingForm(instance=saved_address)
    if request.method == 'POST':
        form = BillingForm(request.POST, instance=saved_address)
        if form.is_valid():
            form.save()
            form = BillingForm(instance=saved_address)
            messages.success(request, f"Shipping Address Saved!")
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].orderitems.all()
    order_total = order_qs[0].get_totals()
    return render(request, 'App_Payment/checkout.html', context={'form': form, 'order_items': order_items,
                                                                 'order_total': order_total,
                                                                 'saved_address': saved_address})


@login_required
def payment(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    if not saved_address.is_fully_filled():
        messages.info(request, f'Please Complete shipping address!')
        return redirect("App_Payment:CheckOut")
    if not request.user.profile.is_fully_filled():
        messages.info(request, f"Please Complete Your Profile details!")
        return redirect('App_Login:profile')
    store_id = 'abcli60ee58b669c34'
    API_KEY = 'abcli60ee58b669c34@ssl'
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id,
                            sslc_store_pass=API_KEY)
    status_url = request.build_absolute_uri(reverse('App_Payment:complete'))
    mypayment.set_urls(success_url=status_url, fail_url=status_url,
                       cancel_url=status_url, ipn_url=status_url)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].orderitems.all()
    order_items_count = order_qs[0].orderitems.count()
    order_total = order_qs[0].get_totals()
    mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT', product_category='Mixed',
                                      product_name=order_items, num_of_item=order_items_count, shipping_method='Courier',
                                      product_profile='None')
    current_user = request.user
    mypayment.set_customer_info(name=current_user.profile.full_name, email=current_user.email, address1=current_user.profile.address_1,
                                address2=current_user.profile.address_1, city=current_user.profile.city,
                                postcode=current_user.profile.zipcode, country=current_user.profile.country,
                                phone=current_user.profile.phone)

    mypayment.set_shipping_info(shipping_to=current_user.profile.user, address=saved_address.address,
                                city=saved_address.city, postcode=saved_address.zipcode,
                                country=saved_address.country)
    response_data = mypayment.init_payment()

    return redirect(response_data['GatewayPageURL'])


@csrf_exempt
def complete(request):
    if request.method == 'POST' or request.method == 'post':
        payment_date = request.POST
        status = payment_date['status']
        if status == 'VALID':
            val_id = payment_date['val_id']
            tran_id = payment_date['tran_id']
            messages.success(request, f"Your Payment Completed Successfully! Page will be redirected!")
            return HttpResponseRedirect(
                reverse("App_Payment:purchase", kwargs={'val_id': val_id, 'tran_id': tran_id}, ))
        elif status == 'FAILED':
            messages.warning(request, f"Your Payment Failed! Please Try Again! Page will be redirected!")
    return render(request, 'App_Payment/complete.html', context={})


@login_required
def purchase(request, val_id, tran_id):
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order = order_qs[0]
    orderId = tran_id
    order.ordered = True
    order.orderId = orderId
    order.paymentId = val_id
    order.save()
    cart_items = Cart.objects.filter(user=request.user, purchased=False)
    for item in cart_items:
        item.purchased = True
        item.save()
    return HttpResponseRedirect(reverse("App_Shop:Home"))


@login_required
def order_view(request):
    try:
        orders = Order.objects.filter(user=request.user, ordered=True)
        context = {"orders": orders}
    except:
        messages.warning(request, "You do no have an active order")
        return redirect("App_Shop:Home")
    return render(request, "App_Payment/order.html", context)
