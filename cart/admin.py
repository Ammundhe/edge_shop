from django.contrib import admin
from cart.models import Cart, couponCode



class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity']
    search_fields = ['product__name', 'user__first_name']

class couponCodeAdmin(admin.ModelAdmin):
    list_display=('code', 'discount',)
    search_fields=['code']

admin.site.register(Cart, CartAdmin)

admin.site.register(couponCode, couponCodeAdmin)