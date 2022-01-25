from django.db import models

class productCategory(models.Model):
    """product category"""
    name=models.CharField(max_length=255)
    status=models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.name)

class product(models.Model):
    """product models"""
    product_category=models.ForeignKey(productCategory, on_delete=models.CASCADE, related_name='ProductCategory')
    name=models.CharField(max_length=255)
    decriptions=models.TextField()
    price=models.DecimalField(max_digits=8, decimal_places=2)
    stock=models.IntegerField()
    cover_image=models.ImageField()
    status=models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.name)

class productImage(models.Model):
    """product image models """
    product=models.ForeignKey(product, on_delete=models.CASCADE)
    image=models.ImageField()

    def __str__(self) -> str:
        return str(self.product)
