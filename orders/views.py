import random

from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect

from account.models import ShopUser
from orders.forms import PhoneVerificationForm


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