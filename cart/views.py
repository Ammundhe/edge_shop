from django.shortcuts import redirect, render
from django.views import View
from cart.models import Cart, couponCode
from product.models import product, productCategory
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import razorpay
from django.http.response import HttpResponse, JsonResponse
from order.models import order, orderDetail
from payment.models import Payment
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt


class AddtoCart(View):
    
    def post(self, request):
        quantity = request.POST.get('quantity')
        product_id = request.POST.get('product_id')
        cart, created = Cart.objects.get_or_create(product_id=product_id, user_id=request.user.id)
        if product_id:
            Product=product.objects.get(id=product_id)
            Product.stock=int(Product.stock)-int(quantity)
            Product.save()
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
        sub_total=shippingcost+subtotal
        if request.GET.get('coupon'):
            coupon_code=request.GET.get('coupon')
            couponcode=couponCode.objects.get(code=coupon_code)
            total=float(sub_total)-(float(sub_total*couponcode.discount))
            context={
                'navigationCategories':navigationCategories,
                'carts':list(cartDate.values()),
                'subtotal':subtotal,
                'total':total,
                'shippingCost':shippingcost
            }
            return render(request, self.template_name, context)
        else:
            total=sub_total

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
            total=subtotal+shippingCost
        context={
            'navigationCategories':navigationCategories,
            'carts':list(cartData.values()),
            'subtotal':subtotal,
            'shippingCost':shippingCost,
            'total':total
        }
        return render(request, self.template_name, context)

    def post(self, request):
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        address=request.POST.get('address')
        carts=Cart.objects.filter(user=request.user)
        cartData={}
        subtotal=0
        shippingCost=50
        total=0
        for key, cart in enumerate(carts):
            productTotal=int(cart.product.price)*int(cart.quantity)
            subtotal+=productTotal
            total+=productTotal
        total=(subtotal+shippingCost)*100
        client = razorpay.Client(auth=("rzp_test_k6sHZT5YbqmvML", "xzGWzEec17JFycss2MFMTitH"))
        receipt=f'order_rcptid_{request.user.id}'
        data = { "amount": total, "currency": "INR", "receipt": receipt }
        payment = client.order.create(data=data)
        if payment.get('id'):
            context={
                'order_id':payment['id'],
                'amount':payment['amount'],
                'first_name': first_name,
                'last_name':last_name,
                'address':address,
            }
            return render(request, 'capture-payment.html', context)
    
class PaymentSuccess(View):

    def post(self, request):
        razorpay_payment_id=request.POST.get('razorpay_payment_id')
        razorpay_order_id= request.POST.get('razorpay_order_id')
        razorpay_signature= request.POST.get('razorpay_signature')
        first_name= request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        address =request.POST.get('address')
        carts=Cart.objects.filter(user=request.user)
        if carts:
            orders=order.objects.create(
                user=request.user,
                name=f'{first_name} {last_name}',
                address=address,
                date_time=datetime.now(),
                razor_pay_order_id=razorpay_order_id,

            )
            for cart in carts:
                print(cart)
                orderDetail.objects.create(
                    order=orders,
                    product=cart.product,
                    quantity=cart.quantity,
                    product_price=cart.product.price,
                )
            carts.delete()
        return JsonResponse({"status":"success"})

@csrf_exempt
def RayzorpayWebhook(request):
    requestBody = json.load(request.body.decode('utf-8'))
    payload = requestBody['payload']
    if payload['payment']:
        order_id = payload['payment']['entity']['order_id']
        try:
            order = order.objects.get(razor_pay_order_id=order_id)
            payment = Payment.objects.get_or_create(order=order)
            payment.payment_id=payload['payment']['entity']['id']
            payment.payment_status=payload['payment']['entity']['status']
            payment.payment_method=payload['payment']['entity']['method']
            payment.created_at=payload['payment']['entity']['created_at']
            payment.amount=payload['payment']['entity']['amount']
            payment.save()
            order.payment_status=True
            order.save()
            return JsonResponse({'status':'success'})
        except:
            return JsonResponse({'status':'failed'})

def ThankYou(request):
    return HttpResponse('<h1>Thank You, Your order has been placed! </h1>')