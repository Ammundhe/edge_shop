from dataclasses import fields
from pyexpat import model
from django.forms import ModelForm
from django.contrib.auth.models import User
from user_profile.models import user_profile


class Userform(ModelForm):
    class Meta:
        model=User
        fields=['first_name', 'last_name','email']


class User_profileform(ModelForm):
    class Meta:
        model=user_profile
        fields=['adress', 'mobile','profile_picture']