from django.shortcuts import render
from category.models import *
from products.models import *
from banner.models import *
from social_core.backends.google import GoogleOAuth2

# Create your views here.
def home(request):
    banner = Banner.objects.all()
    context={
        'banners':banner,
    }
    return render(request,'user\home\home.html',context)

def login(request):
    return render(request,'user/accounts/registration.html')
