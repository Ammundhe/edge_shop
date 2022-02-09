from django.contrib import admin, messages
from .models import product, productCategory, productImage

def markas_inactive(self, request, queryset):
    queryset.update(status=False)
    messages.success(request, 'selected record(s) marked as inactive')

def markas_active(self, request, queryset):
    queryset.update(status=True)
    messages.success(request, 'selected record(s) marked as active')

def stock_available(self, request, queryset):
    queryset.update(stock_status='Available')
    messages.success(request, 'selected record(s) marked as Available')

def stock_Notavailable(self, request, queryset):
    queryset.update(stock_status='Not Available')
    messages.success(request, 'selected record(s) marked as Not Available')


class productcategoryAdmin(admin.ModelAdmin):
    list_display=('name','status')
    list_filter=('status',)
    search_fields=('name',)
    actions=[markas_inactive, markas_active,]

admin.site.register(productCategory,productcategoryAdmin)



class prodcutImageAdmin(admin.TabularInline):
    model=productImage
    extra=1
    classes=('collapse',)

class productAdmin(admin.ModelAdmin):
    list_display=['name','price', 'stock', 'status', 'stock_status']
    list_filter=['status', 'stock_status']
    search_fields=['name','price','stock']
    actions=[markas_active,markas_inactive,stock_available, stock_Notavailable]
    inlines=[prodcutImageAdmin]


admin.site.register(product,productAdmin)    