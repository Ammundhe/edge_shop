from django.urls import path
from . import views

urlpatterns = [
    path('add-to-cart', views.AddtoCart.as_view(), name="AddtoCart"),
    path('my-cart',views.Mycart.as_view(), name="Mycart"),
    path('checkout', views.Checkout.as_view(), name="Checkout"),
    path('payment-success', views.PaymentSuccess.as_view(), name="PaymentSuccess"),
    path('webhooks', views.RayzorpayWebhook, name=
        "RayzorpayWebhook"),
    path('thank-you', views.ThankYou, name="ThankYou")
    
]