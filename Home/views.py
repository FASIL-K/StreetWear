from django.shortcuts import render
from category.models import *
from products.models import *
from social_core.backends.google import GoogleOAuth2

# Create your views here.
def home(request):
    return render(request,'user\home\home.html')

def login(request):
    return render(request,'user/accounts/registration.html')
