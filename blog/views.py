from re import search
from django.shortcuts import render
from django.views import View
from product.models import productCategory
from .models import BlogCategory, BlogPost


class Blogcategory(View):

    template_name='blog.html'

    def get(self, request, blogCategory_id=None):
        if request.GET.get('search'):
            search=request.GET.get('search')
            blogPost=BlogPost.objects.filter(title__icontains=search)
            navigationCategories=productCategory.objects.filter(status=True)
            blogCategories=BlogCategory.objects.all()
            context={
                'navigationCategories':navigationCategories,
                'blogCategories':blogCategories,
                'blogPost':blogPost,
            }
            return render(request, self.template_name, context)
            
        if blogCategory_id:
            navigationCategories=productCategory.objects.filter(status=True)
            blogCategories=BlogCategory.objects.all()
            blogPost=BlogPost.objects.filter(category_id=blogCategory_id)
            context={
                'navigationCategories':navigationCategories,
                'blogCategories':blogCategories,
                'blogPost':blogPost,
            }
            return render(request, self.template_name, context)
        
        blogPost=BlogPost.objects.all()
        navigationCategories=productCategory.objects.filter(status=True)
        blogCategories=BlogCategory.objects.all()
        context={
            'navigationCategories':navigationCategories,
            'blogCategories':blogCategories,
            'blogPost':blogPost,
        }
        return render(request, self.template_name, context)

class PostDetail(View):
    template_name='blog-details.html'

    def get(self, request, slug):
        navigationCategories=productCategory.objects.filter(status=True)
        try:
            blogCategories=BlogCategory.objects.all()
            blogPost=BlogPost.objects.get(slug=slug)

        except:
            blogCategories={}
            blogPost={}
        
        context={
            'navigationCategories':navigationCategories,
            'blogCategories':blogCategories,
            'blogPost':blogPost,
            'slug':slug,
        }
        return render(request, self.template_name, context)