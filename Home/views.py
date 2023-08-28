from django.shortcuts import render,redirect
from category.models import *
from products.models import *
from banner.models import *
from social_core.backends.google import GoogleOAuth2
from cart.views import transfer_guest_cart_to_authenticated_user
from django.contrib.auth import get_user_model


# Create your views here.
def home(request):
    banner = Banner.objects.all()
    context={
        'banners':banner,
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
        transfer_guest_cart_to_authenticated_user(request, user)
        return redirect('home')  # Redirect to the home page after successful login
    else:
        # Handle case where user is not authenticated (optional)
        # For example, redirect them to the login page
        return redirect('login')


