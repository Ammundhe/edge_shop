from django.contrib import admin, messages
from .models import product, productCategory, productImage

def markas_inactive(self, request, queryset):
    queryset.update(status=False)
    messages.success(request, 'selected record(s) marked as inactive')

def markas_active(self, request, queryset):
    queryset.update(status=True)
    messages.success(request, 'selected record(s) marked as active')


class productcategoryAdmin(admin.ModelAdmin):
    list_display=('name','status')
    list_filter=('status',)
    search_fields=('name',)
    actions=[markas_inactive, markas_active]

admin.site.register(productCategory,productcategoryAdmin)



class prodcutImageAdmin(admin.TabularInline):
    model=productImage
    extra=1
    classes=('collapse',)

class productAdmin(admin.ModelAdmin):
    list_display=['name','price', 'stock', 'status']
    list_filter=['status']
    search_fields=['name','price','stock']
    actions=[markas_active,markas_inactive]
    inlines=[prodcutImageAdmin]


admin.site.register(product,productAdmin)    