from io import StringIO

import openpyxl
from django.contrib import admin
from django.http import HttpResponse, StreamingHttpResponse

from .models import Orders,OrderItem
from cart.common.KaveSms import send_sms_normal
import csv
from django.http import HttpResponse

# Register your models here.

def export_to_excel(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=orders.xlsx'
    # --------------------
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Orders"
    # --------------------
    columns = ['ID', 'First Name', 'Last Name', 'Phone', 'Address', 'Postal Code',
               'Province', 'City', 'Paid', 'Created']
    ws.append(columns)
    # --------------------
    for order in queryset:
        created = order.created.replace(tzinfo=None) if order.created else ''
        ws.append([
            order.id, order.first_name, order.last_name, order.phone, order.address,
            order.postal_code, order.province, order.city, order.paid, created
        ])
    wb.save(response)
    return response

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    raw_id_fields= ['product']

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ['buyer','first_name', 'last_name','address', 'city', 'postal_code',
                    'phone', 'province', 'created', 'updated', 'paid', 'status']
    list_filter = ['paid', 'created', 'updated']
    list_editable = ['status']
    inlines = [OrderItemInline]
    actions = [export_to_excel]
