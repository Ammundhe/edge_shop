from django.contrib import admin
from cart.models import Cart



class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity']
    search_fields = ['product__name', 'user__first_name']

admin.site.register(Cart, CartAdmin)