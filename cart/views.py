from django.shortcuts import redirect, render
from django.views import View
from cart.models import Cart
from product.models import productCategory
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


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

@method_decorator(login_required, name="dispatch")
class Mycart(View):


    template_name='my-cart.html'

    def get(self,request):
        navigationCategories=productCategory.objects.filter(status=True)
        carts=Cart.objects.filter(user=request.user)
        cartDate={}
        subtotal=0
        total=0
        shippingcost=50

        for key,cart in enumerate(carts):
            productTotal=int(cart.product.price)*int(cart.quantity)
            subtotal+=productTotal
            cartDate[key]={
                'product_image':cart.product.cover_image,
                'product_name':cart.product.name,
                'product_price':cart.product.price,
                'quantity':cart.quantity,
                'product_Total':productTotal,
                'cart_id':cart.id
            }
        total=shippingcost+subtotal
        context={
            'navigationCategories':navigationCategories,
            'carts':list(cartDate.values()),
            'subtotal':subtotal,
            'total':total,
            'shippingCost':shippingcost
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        cart_id_list=request.POST.getlist('card_id')      
        quantity_list=request.POST.getlist('quantity')
        for index, cart_id in enumerate(cart_id_list):
            try:
                cartObject=Cart.objects.get(id=cart_id)
                if int(quantity_list[index])==0:
                    cartObject.delete()
                else:
                    cartObject.quantity=quantity_list[index]
                    cartObject.save()
            except Cart.DoesNotExist:
                pass

        return redirect('Mycart')


@method_decorator(login_required, name="dispatch")
class Checkout(View):

    template_name='checkout.html'

    def get(self, request):
        navigationCategories=productCategory.objects.filter(status=True)
        carts=Cart.objects.filter(user=request.user)
        cartData={}
        subtotal=0
        shippingCost=50
        total=0
        for key, cart in enumerate(carts):
            productTotal=int(cart.product.price)*int(cart.quantity)
            subtotal+=productTotal
            cartData[key]={
                'product_name':cart.product.name,
                'product_total':productTotal,
            }
            print(subtotal)
            total=subtotal+shippingCost
        context={
            'navigationCategories':navigationCategories,
            'carts':list(cartData.values()),
            'subtotal':subtotal,
            'shippingCost':shippingCost,
            'total':total
        }
        return render(request, self.template_name, context)

    