from turtledemo.penrose import start

from django.contrib import messages
from django.contrib.auth.password_validation import password_changed
from django.contrib.sites import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PhoneVerificationForm, OrderCreateForm
from account.models import ShopUser
from .models import OrderItem, Orders
from cart.cart import Cart
import random
from cart.common.KaveSms import send_sms_with_template
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse, Http404
import requests
import json
from datetime import datetime
# Create your views here.

def verify_phone(request):
    if request.user.is_authenticated:
        return redirect('orders:create_order')

    if request.method == "POST":
        form = PhoneVerificationForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            if ShopUser.objects.filter(phone=phone).exists():
                messages.error(request, "Phone number already registered")
                return redirect('orders:verify_phone')
            else:
                tokens = {'tokens': ''.join(random.choices('1234567890', k=6))}
                request.session['verification_code'] = tokens['tokens']

                request.session['phone'] = phone
                #send_sms_with_template(phone, tokens, 'verify')

                messages.error(request, "verification code send successfully")
                return redirect('orders:verify_code')

    else:
        form = PhoneVerificationForm()
    return render(request, 'verify_phone.html', {'form': form})


def verify_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        if code:
            verification_code = request.session['verification_code']
            phone = request.session['phone']
            if code == verification_code:
                user = ShopUser.objects.create_user(phone=phone)
                user.set_password('123456')
                user.save()
                # send sms
                login(request, user)
                del request.session['verification_code']
                del request.session['phone']
                return redirect('orders:order_create')
            else:
                messages.error(request, 'Verification code is incorrect.')
    return render(request, 'verify_code.html')


@login_required
def create_order(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            order.buyer = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                             price=item['price'], quantity=item['quantity'],
                                             weight=item['weight'])
            cart.clear()
            # request.session['order_id'] = order.id
            return redirect('orders:request')
    else:
        form = OrderCreateForm(current_user=request.user)
    return render(request, 'create_order.html', {'form': form, 'cart': cart})

if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

CallbackURL = 'http://127.0.0.1:8000/order/verify/'


def send_request(request):
    order = Orders.objects.get(id=request.session['order_id'])
    description = ""
    for item in order.items.all():
        description += item.product.name + ", "
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": order.get_final_cost(),
        "Description": description,
        "Phone": request.user.phone,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'accept': 'application/json', 'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response_json = response.json()
            authority = response_json['Authority']
            if response_json['Status'] == 100:
                return redirect(ZP_API_STARTPAY + authority)
            else:
                return HttpResponse('Error')
        return HttpResponse('response failed')
    except requests.exceptions.Timeout:
        return HttpResponse('Timeout Error')
    except requests.exceptions.ConnectionError:
        return HttpResponse('Connection Error')


def verify(request):
    order = Orders.objects.get(id=request.session['order_id'])
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": order.get_final_cost(),
        "Authority": request.GET.get('Authority'),
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'accept': 'application/json', 'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
        if response.status_code == 200:
            response_json = response.json()
            reference_id = response_json['RefID']

            if response_json['Status'] == 100:
                for item in order.items.all():
                    item.product.inventory -= item.quantity
                    item.product.save()
                order.paid = True
                order.save()
                return render(request, 'payment-tracking.html',
                              {"success": True, 'RefID': reference_id, "order_id": order.id})
            else:
                return render(request, 'payment-tracking.html',
                              {"success": False, })
        del request.session['order_id']
        return HttpResponse('response failed')
    except requests.exceptions.Timeout:
        return HttpResponse('Timeout Error')
    except requests.exceptions.ConnectionError:
        return HttpResponse('Connection Error')