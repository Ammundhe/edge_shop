from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import authentication
from rest_framework import status
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.views import APIView
from rest_framework.settings import api_settings
from django.contrib.auth.models import User

from order.models import order
from .serializers import user_serializer, productCategorySerializer,productSerializer, CartSerializer, orderSerializer, blogCategorySerializer,blogPostserializer
from product.models import productCategory, product
from cart.models import Cart
from blog.models import BlogCategory, BlogPost



class LoginPage(ObtainAuthToken):
    renderer_classes=api_settings.DEFAULT_RENDERER_CLASSES

class signup(ModelViewSet):
    serializer_class=user_serializer
    queryset=User.objects.filter(is_superuser=False, is_staff=False)

class productCategory(ModelViewSet):
    http_method_names=['get']
    serializer_class=productCategorySerializer
    queryset=productCategory.objects.filter(status=True)

class productview(ModelViewSet):
    http_method_names=['get']
    serializer_class=productSerializer
    queryset=product.objects.filter(status=True)
    filter_backends=[filters.SearchFilter, filters.OrderingFilter]
    search_fields=('name', 'product_category',)
    ordering_fields=('price',)

class CartView(APIView):
    authentication_class=[authentication.TokenAuthentication]
    permission_class=[IsAuthenticated]
    serializer_class=CartSerializer

    def get(self, request):
        queryset=Cart.objects.filter(user=request.user)
        serializer=self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            product_id=serializer.validated_data.get('product')
            quantity=serializer.validated_data.get('quantity')
            cart, create=Cart.objects.get_or_create(product=product_id, user=request.user)
            cart.quantity=int(quantity)
            if product_id:
                Product=product.objects.get(name=product_id)
                Product.stock=int(Product.stock)-int(quantity)
                Product.save()
            if quantity==0:
                cart.delete()
            else:
                cart.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def detele(self, request, cartid=None):
        if cartid:
            try:
                cart=Cart.objects.get(id=cartid).delete()
                return Response({'details':'sucess'})
            except Cart.DoesNotExist:
                return Response({'details':'Not found'}, status=status.HTTP_404_NOT_FOUND) 
        return Response({'datails':'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)

class checkoutView(APIView):
    authentication_class=(authentication.TokenAuthentication)
    permission_class=(IsAuthenticated)

    def get(self, request):
        try:
            cart=Cart.objects.filter(user=request.user)

        except:
            pass

class orderview(ViewSet):
    authentication_class=[authentication.TokenAuthentication]
    permission_class=[IsAuthenticated]
    serializer_class=orderSerializer
    queryset=order.objects.all()

    def list(self, request):
        queryset=order.objects.filter(user=request.user)
        serializer=self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self,request, pk):
        queryset=order.objects.get(pk=pk, user=request.user)
        serializer=self.serializer_class(queryset)
        return Response(serializer.data)

class blogCategoryview(ModelViewSet):
    http_method_names=['get']
    serializer_class=blogCategorySerializer
    queryset=BlogCategory.objects.all()

class blogPostview(ModelViewSet):
    serializer_class=blogPostserializer
    queryset=BlogPost.objects.all()
