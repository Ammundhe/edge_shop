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
        searchdict={
            "status":True
            
            }
        if product_category_id:
            searchdict['product_category_id']=product_category_id
        if request.GET.get('search'):
            searchdict['name__icontains']=request.GET.get('search')
        
        if request.GET.get('min'):
            searchdict['price__gte']=request.GET.get('min').replace('₹','')
        if request.GET.get('max'):
            searchdict['price__lte']=request.GET.get('max').replace('₹', '')

        if request.GET.get('sorting'):

            if request.GET.get('sorting')=='low':
                Product=product.objects.filter(**searchdict).order_by('price')
            if request.GET.get('sorting')=='high':
                Product=product.objects.filter(**searchdict).order_by('-price')
        else:
            Product=product.objects.filter(**searchdict)
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