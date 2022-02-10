from django.urls import path, include
from django.db import router
from rest_framework.routers import DefaultRouter
from . import views

router=DefaultRouter()

router.register('signup', views.signup)
router.register('product-category', views.productCategory)
router.register('product', views.productview)
router.register('order', views.orderview)
router.register('blog-category', views.blogCategoryview)
router.register('blog-post', views.blogPostview)

urlpatterns = [
    path('login', views.LoginPage.as_view()),
    path('mycart', views.CartView.as_view()),
    path('mycart/<int:cartid>', views.CartView.as_view()),
    path('', include(router.urls)),
]
