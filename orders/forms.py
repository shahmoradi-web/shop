from django import forms

from account.models import ShopUser
from .models import Orders
class PhoneVerificationForm(forms.Form):
    phone = forms.CharField(label='Phone Number', max_length=11)