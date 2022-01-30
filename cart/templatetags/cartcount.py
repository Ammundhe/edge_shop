from django import template
from cart.models import Cart
from django.db.models import Sum

register=template.Library()


@register.simple_tag
def cartCount(request):
    """display cart count base on current user's session"""
    if request.user.is_authenticated:
        carts=Cart.objects.filter(user=request.user).aggregate(cart_sum=Sum('quantity'))
        return carts['cart_sum']

    return 0