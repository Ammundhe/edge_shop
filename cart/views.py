from django.shortcuts import redirect
from django.views import View
from cart.models import Cart



class AddtoCart(View):
    
    def post(self, request):
        quantity = request.POST.get('quantity')
        product_id = request.POST.get('product_id')
        cart, created = Cart.objects.get_or_create(product_id=product_id, user_id=request.user.id)
        if created:
            cart.quantity = quantity
        else:
            cart.quantity = int(quantity) + int(cart.quantity)
        cart.save()
        # try:
        #     cart = Cart.objects.get(product_id=product_id, user_id=request.user.id)
        #     cart.quantity = int(quantity) + int(cart.quantity)
        #     cart.save()
        # except Cart.DoesNotExist:
        #     Cart.objects.create(
        #         quantity=quantity,
        #         product_id=product_id,
        #         user=request.user
        #     )
        return redirect('productDetail', product_id=product_id)