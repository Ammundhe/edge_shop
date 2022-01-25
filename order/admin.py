from django.contrib import admin, messages
from .models import order, orderDetail

def mark_as_pending(self, request, queryset):
    queryset.update(order_status='pending')
    messages.success(request, 'selected record(s) marked as pending')

def mark_as_inprogress(self, request, queryset):
    queryset.update(order_status='inprogress')
    messages.success(request, 'selected record(s) marked as inprogress')

def mark_as_Delivered(self, request, queryset):
    queryset.update(order_status='Delivered')
    messages.success(request, 'selected record(s) marked as Delivered')

def mark_as_cancelled(self, request, queryset):
    queryset.update(order_status='cancelled')
    messages.error(request, 'selected record(s) marked as cancelled')

class orderDetailAdmin(admin.TabularInline):
    model=orderDetail
    extra=1

class orderAdmin(admin.ModelAdmin):
    list_display=['user','name','order_status','payment_status']
    list_filter=['order_status','payment_status']
    search_fields=['user','name',]
    actions=[mark_as_pending,mark_as_inprogress,mark_as_Delivered,mark_as_cancelled]
    inlines=[orderDetailAdmin]


admin.site.register(order, orderAdmin)
