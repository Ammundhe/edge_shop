from django.shortcuts import render
from django.views import View
from product.models import productCategory
from order.models import order, orderDetail

class Orderdetails(View):
    template_name='order-detail.html'

    def get(self, request):
        navigationCategories=productCategory.objects.filter(status=True)
        user_order=order.objects.get(user_id=request.user)
        user_orderdetails=orderDetail.objects.get(order_id=user_order)
        context={
            'navigationCategories':navigationCategories,
            'user_order':user_order,
            'user_orderdetails':user_orderdetails,
        }
        return render(request, self.template_name, context)
