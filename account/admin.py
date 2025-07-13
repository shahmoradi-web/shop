from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import ShopUser


# Register your models here.

@admin.register(ShopUser)
class ShopUserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name','phone','is_staff','is_active']


