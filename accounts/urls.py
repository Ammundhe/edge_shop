from django.urls import path
from accounts import views

urlpatterns = [
    path('login', views.Login.as_view(), name='Login'),
    path('logout',views.Logout, name='Logout')
]
