from django.shortcuts import redirect, render
from django.views import View
from product.models import productCategory
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import login as Authlogin, authenticate
from django.contrib.auth import logout as Authlogout
from user_profile.models import user_profile
from user_profile.models import user_profile
from .forms import Userform,User_profileform


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
            if request.POST.get('next') !='None':
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
    user=Userform
    navigationCategories=productCategory.objects.filter(status=True)

    def get(self, request):
        userform=self.user()
        context={
            'navigationCategories':self.navigationCategories,
            'userform':userform,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        user_info=self.user(data=request.POST, instance=request.user)
        if user_info.is_valid():
            user_info.save()
            return redirect("userProfile")
        return redirect("updateProfile")

class userProfile(View):
    template_name='user-profile.html'
    user_profile=User_profileform
    navigationCategories=productCategory.objects.filter(status=True)

    def get(self, request):
        user_profileform=self.user_profile()
        context={
            'navigationCategories':self.navigationCategories,
            'user_profileform':user_profileform
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        adress=request.POST.get('adress')
        mobile=request.POST.get('mobile')
        profile_picture=request.POST.get('profile_picture')
        user_profile.objects.create(
            user=request.user,
            adress=adress,
            mobile=mobile,
            profile_picture=profile_picture
        )
        return redirect("userProfile")