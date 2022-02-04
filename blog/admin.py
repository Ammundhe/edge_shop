from django.contrib import admin
from .models import BlogCategory, BlogPost

class BlogCategoryAdmin(admin.ModelAdmin):
    list_display=['name', 'status']
    list_filter=['status']
    search_fields=['name']

admin.site.register(BlogCategory,BlogCategoryAdmin)

class BlogPostAdmin(admin.ModelAdmin):
    list_display=['title', 'date']
    search_fields=['title']

admin.site.register(BlogPost,BlogPostAdmin)
