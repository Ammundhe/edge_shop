from django.urls import path
from . import views


urlpatterns = [
    path('post', views.Blogcategory.as_view(), name="NewPost" ),
    path('post/<int:blogCategory_id>', views.Blogcategory.as_view(), name="NewPost" ),
    path('post/<str:slug>',views.PostDetail.as_view(), name="BlogPost")
]
