from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.forms import ShopUserCreationForm, ShopUserChangeForm
from account.models import ShopUser



# Register your models here.

@admin.register(ShopUser)
class ShopUserAdmin(admin.ModelAdmin):
    ordering = ['phone']
    add_form = ShopUserCreationForm
    form = ShopUserChangeForm
    model = ShopUser
    list_display = ['phone', 'first_name', 'last_name', 'is_active', 'is_staff']
    fieldsets = (
        (None,{'fields': ('phone','password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'address')}),
        ('Permission', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'fields': ('phone', 'password1', 'password2')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'address')}),
        ('Permission', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
