from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from account.models import ShopUser


class ShopUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = ShopUser
        fields = ('phone', 'first_name', 'last_name', 'address', 'is_active', 'is_staff',)

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")

        if self.instance.pk:
            if ShopUser.objects.filter(phone=phone).exclude(id=self.instance.pk).exists():
                raise forms.ValidationError("This phone number is already in use.")
        else:
            if ShopUser.objects.filter(phone=phone).exists():
                raise forms.ValidationError("This phone number is already in use.")
        if not phone.isdigit():
            raise forms.ValidationError("Please enter a valid phone number.")
        if not phone.startswith('09'):
            raise forms.ValidationError("phone must start with '09'.")
        if len(phone) != 11:
            raise forms.ValidationError("phone must have be 11 digits.")
        return phone



class ShopUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = ShopUser
        fields = ('phone', 'first_name', 'last_name', 'address', 'is_active', 'is_staff')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if self.instance.pk:
            if ShopUser.objects.filter(phone=phone).exclude(id=self.instance.pk).exists():
                raise forms.ValidationError("This phone number is already in use.")
        else:
            if ShopUser.objects.filter(phone=phone).exists():
                raise forms.ValidationError("This phone number is already in use.")
        if not phone.isdigit():
            raise forms.ValidationError("Please enter a valid phone number.")
        if not phone.startswith('09'):
            raise forms.ValidationError("phone must start with '09'.")
        if len(phone) != 11:
            raise forms.ValidationError("phone must have be 11 digits.")
        return phone
