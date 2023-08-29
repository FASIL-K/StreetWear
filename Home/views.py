from django.shortcuts import render,redirect
from category.models import *
from products.models import *
from banner.models import *
from social_core.backends.google import GoogleOAuth2
from cart.views import transfer_guest_cart_to_authenticated_user
from django.contrib.auth import get_user_model
from social_django.models import UserSocialAuth
from django.contrib.auth import login


# Create your views here.
def home(request):
    banner = Banner.objects.all()
    products =Product.objects.all()
    context={
        'banners':banner,
        'products':products

    }
    return render(request,'user\home\home.html',context)

# def custom_login(request):
#     transfer_guest_cart_to_authenticated_user(request, user)

#     return render(request,'user/accounts/registration.html')
User = get_user_model()  # Get the user model

def custom_login(request):
    user = request.user  # Get the authenticated user
    print(user,'google auth')
    if user.is_authenticated:
        try:
            social_auth = user.social_auth.get(provider='google-oauth2')
            print("User has Google OAuth authentication")

        except UserSocialAuth.DoesNotExist:
            social_auth = None
        
        if social_auth:
            transfer_guest_cart_to_authenticated_user(request, user)
            login(request, user)
            return redirect('home')
    else:
        return redirect('signin')

