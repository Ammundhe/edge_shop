from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name="Homepage"),
    path('productlisting/<int:product_category_id>', views.ProductListing.as_view(), name="Productlisting"),
    path('productdetails/<int:product_id>', views.productDetail.as_view(), name="productDetail"),
]
