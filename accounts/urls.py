from django.urls import path
from accounts import views

urlpatterns = [
    path('login/', views.Login.as_view(), name='Login'),
    path('logout',views.Logout, name='Logout'),
    path('create-account', views.create_account.as_view(), name="Create_account"),
    path('personal-info', views.update_profile.as_view(), name="updateProfile"),
    path('user-profile', views.userProfile.as_view(), name="userProfile"),
]
