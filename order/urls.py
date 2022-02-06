from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('order-details', views.Orderdetails.as_view(), name="orderDetail")
]
