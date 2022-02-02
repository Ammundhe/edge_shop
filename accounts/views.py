from datetime import date
import email
from venv import create
from wsgiref.util import request_uri
from django.shortcuts import redirect, render
from django.views import View
from product.models import productCategory
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import login as Authlogin, authenticate
from django.contrib.auth import logout as Authlogout
from .forms import Create_accountform
from django.contrib.auth.models import User


    # User is authenticated

class Login(View):

    template_name='login.html'
    form_class=AuthenticationForm
    navigationCategories=productCategory.objects.filter(status=True)

    def get(self,request):
        form=self.form_class()
        context={
            'navigationCategories':self.navigationCategories,
            'form':form,
            'next':request.GET.get('next'),
        }
        return render(request, self.template_name,context )

    def post(self, request):
        form=self.form_class(data=request.POST)
        if form.is_valid():
            Authlogin(request, form.get_user())
            if request.POST.get('next'):
                return redirect(request.POST.get('next'))
            return redirect('Homepage')

        context={
            'navigationCategories':self.navigationCategories,
            'form':form,
            }
        return render(request, self.template_name,context )

def Logout(request):
    Authlogout(request)
    return redirect('Homepage')


class create_account(View):
    template_name='create-account.html'
    form_class=UserCreationForm
    navigationCategories=productCategory.objects.filter(status=True)


    def get(self, request):
        create_userForm=self.form_class()
        context={
            'navigationCategories':self.navigationCategories,
            'form':create_userForm,
        }
        
        return render(request, self.template_name, context)

    def post(self, request):
        new_account=self.form_class(data=request.POST)
        if new_account.is_valid():
            new_account.save()
            username=new_account.cleaned_data.get('username')
            password=new_account.cleaned_data.get('password1')
            user=authenticate(username=username, password=password)
            Authlogin(request, user)
            return redirect("updateProfile")
        else:
            new_account=self.form_class()
        return redirect("Create_account")
    
class update_profile(View):
    template_name='update-profile.html'
    account=Create_accountform
    navigationCategories=productCategory.objects.filter(status=True)

    def get(self, request):
        person_info=self.account()
        context={
            'navigationCategories':self.navigationCategories,
            'person_info':person_info,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        new_info=self.account(data=request.POST, instance=request.user)
        if new_info.is_valid():
            new_info.save()
            return redirect("Homepage")
        return redirect("updateProfile")