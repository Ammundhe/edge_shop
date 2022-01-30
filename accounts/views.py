from django.shortcuts import redirect, render
from django.views import View
from product.models import productCategory
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as Authlogin
from django.contrib.auth import logout as Authlogout
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


