from django.db import models
from django.contrib.auth.models import User
from product.models import product


class order(models.Model):
    """order model details"""
    order_status_choice=(
        ('pending','pending'),
        ('inprogress','inprogress'),
        ('Delivered','Delivered'),
        ('cancelled','cancelled'),
    )
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    date_time=models.DateTimeField()
    name=models.CharField(max_length=255)
    address=models.TextField()
    payment_status=models.BooleanField(default=True)
    order_status=models.CharField(max_length=255, choices=order_status_choice, default='pending')


    def __str__(self) -> str:
        return str(self.id)


class orderDetail(models.Model):
    """orderdetails model detail"""
    order=models.ForeignKey(order, on_delete=models.CASCADE)
    product=models.ForeignKey(product, on_delete=models.CASCADE)
    quantity=models.IntegerField()
    product_price=models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self) -> str:
        return f'{self.order.id}-{self.product}'

