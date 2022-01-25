from django.shortcuts import render
from django.views import View
from product.models import productCategory, product, productImage

class HomePage(View):

    def get(self,request):
        navigationCategories=productCategory.objects.filter(status=True)
        productCategories=productCategory.objects.filter(status=True).order_by('-id')[:3]
        context={
            'navigationCategories':navigationCategories,
            'productCategories':productCategories
        }
        return render(request, 'home-page.html',context)
    
class ProductListing(View):

    template_name='product-listing.html'
    def get(self, request, product_category_id=None):
        navigationCategories=productCategory.objects.filter(status=True)
        Product=product.objects.filter(status=True, product_category_id=product_category_id)
        context={
            'navigationCategories':navigationCategories,
            'Product':Product,
            'product_category_id':product_category_id,
        }
        return render(request, self.template_name, context)  

class productDetail(View):

    template_name="product-detail.html"

    def get(self, request,product_id):
        navigationCategories=productCategory.objects.filter(status=True)
        try:
            Product=product.objects.get(pk=product_id)
            relatedProduct=product.objects.filter(status=True, product_category_id=Product.product_category_id).exclude(id=product_id)
        except product.DoesNotExist:
            Product={}
            relatedProduct={}
        ProductImage=productImage.objects.filter(product_id=product_id)
        context={
            'navigationCategories':navigationCategories,
            'Product':Product,
            'ProductImage':ProductImage,
            'relatedProduct':relatedProduct,
        }
        return render(request, self.template_name, context) 