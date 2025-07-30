from django import forms

from account.models import ShopUser
from .models import Orders
class PhoneVerificationForm(forms.Form):
    phone = forms.CharField(label='Phone Number', max_length=11)


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['first_name', 'last_name', 'phone',
                  'address', 'city', 'province', 'postal_code']

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)
