from django.contrib import admin
from .models import OrderItem,Orders
# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    raw_id_fields= ['product']

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ['id','first_name', 'last_name','address', 'city', 'postal_code',
                    'phone', 'province', 'created', 'updated', 'paid', 'status']
    list_filter = ['paid', 'created', 'updated']
    list_editable = ['status']
    inlines = [OrderItemInline]

