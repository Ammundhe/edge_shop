from django.db import models
from django.contrib.auth.models import User
from product.models import product


class Cart(models.Model):
    """ Cart Model """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        """ Example: afsar SAMSUNG S21 FE, Quantity:1"""
        return f'{self.user} {self.product}, - Quantity: {self.quantity}'

class couponCode(models.Model):
    code=models.CharField(max_length=255, null=True, blank=True)
    discount=models.FloatField(max_length=15)

    def __str__(self) -> str:
        return str(self.code)