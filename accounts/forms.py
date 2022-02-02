from dataclasses import fields
from pyexpat import model
from django.forms import ModelForm
from django.contrib.auth.models import User

class Create_accountform(ModelForm):
    class Meta:
        model=User
        fields=['first_name', 'last_name','email']