from django.db import models
from django.contrib.auth.models import User

class user_profile(models.Model):
    """user profile model details"""
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    adress=models.TextField()
    mobile=models.CharField(max_length=10, null=True, blank=True)
    profile_picture=models.ImageField(null=True, blank=True)


    def __str__(self) -> str:
        return str(self.user)

