from django.contrib import admin
from .models import user_profile

class userProfileAdmin(admin.ModelAdmin):
    list_display=['user','mobile']

admin.site.register(user_profile, userProfileAdmin)
