from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.views.decorators.cache import cache_control
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
# verification email
from .models import UserOTP,Mobile_Otp
from django.contrib import auth
from django.core.mail import send_mail
from django.conf import settings
import random
import re
from . import mixins
from django.core.exceptions import ValidationError
from social_core.backends.google import GoogleOAuth2
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import login
from cart.views import transfer_guest_cart_to_authenticated_user
from cart.models import Cart


# Create your views here.

## this for google login 
User = get_user_model()  # Get the user model


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                # Check if the user is a guest before transferring cart items
                transfer_guest_cart_to_authenticated_user(request, user)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
                return render(request, 'user/accounts/registration.html')

    return render(request, 'user/accounts/registration.html')

from cart.models import Cart



def validateEmail(email):
    from django.core.validators import validate_email
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def ValidatePassword(password):
    from django.contrib.auth.password_validation import validate_password
    try:
        validate_password(password)
        return True
    except ValidationError:
        return False
    
def validate_name(value):
    if not re.match(r'^[a-zA-Z\s]*$', value):
        return 'Name should only contain alphabets and spaces'
    
    elif value.strip() == '':
        return 'Name field cannot be empty or contain only spaces' 
    elif User.objects.filter(username=value).exists():
        return 'Usename already exist'
    else:
        return False

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signup(request):
    if request.user.is_authenticated:
        return redirect('home') 
    """ OTP VERIFICATION """

    if request.method == 'POST':
        # Check if 'otp' field is present in the form data
        get_otp = request.POST.get('otp')
        if get_otp:
            # Handle OTP verification
            get_email = request.POST.get('email')
            try:
                userotp = UserOTP.objects.filter(email=get_email).last()
                if int(get_otp) == userotp.otp:
                    user = User.objects.create_user(
                        username=userotp.username,
                        first_name=userotp.first_name,
                        last_name=userotp.last_name,
                        email=userotp.email,
                        password=userotp.password,
                        phone = userotp.phone,
                        
                    )
                    user.backend = f'{ModelBackend.__module__}.{ModelBackend.__qualname__}'  # Set the backend
                    user.save()
                    auth.login(request, user)
                    userotp.delete()  # Remove the used OTP record
                    return redirect('home')
                else:
                    messages.warning(request, 'You entered a wrong OTP')
                    return render(request, 'user/accounts/registration.html', {'otp': True, 'usr': userotp})
            except ObjectDoesNotExist:
                messages.warning(request, 'User not found')
                return render(request, 'user/accounts/registration.html')

        # User registration validation
        else:
            firstname = request.POST['firstname']   
            lastname = request.POST['lastname']  
            name = request.POST['name']
            phone=request.POST['phone']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            # Null values checking
            check = [name, email, password1, password2,phone]
            for value in check:
                if not value:
                    context = {
                        'pre_firstname': firstname,
                        'pre_lastname': lastname,
                        'pre_name': name,
                        'pre_phone':phone,
                        'pre_email': email,
                    }
                    messages.info(request, 'Some fields are empty')
                    return render(request, 'user/accounts/registration.html', context)

            # Validate name
            result = validate_name(name)
            if result is not False:
                context = {
                    'pre_firstname': firstname,
                    'pre_lastname': lastname,
                    'pre_phone':phone,
                    'pre_name': name,
                    'pre_email': email,
                }
                messages.info(request, result)
                return render(request, 'user/accounts/registration.html', context)

            # Validate email
            if not validateEmail(email):
                context = {
                    'pre_firstname': firstname,
                    'pre_lastname': lastname,
                    'pre_phone':phone,
                    'pre_name': name,
                    'pre_email': email,
                }
                messages.info(request, 'Enter a valid email')
                return render(request, 'user/accounts/registration.html', context)

            # Validate password
            if not ValidatePassword(password1):
                context = {
                    'pre_firstname': firstname,
                    'pre_lastname': lastname,
                    'pre_phone':phone,
                    'pre_name': name,
                    'pre_email': email,
                }
                messages.info(request, 'Enter a strong password')
                return render(request, 'user/accounts/registration.html', context)

            # Check if the email already exists in the User model
            if User.objects.filter(email=email).exists():
                context = {
                    'pre_firstname': firstname,
                    'pre_lastname': lastname,
                    'pre_phone':phone,
                    'pre_name': name,
                    'pre_email': email,
                }
                messages.error(request, 'Email already exists')
                return render(request, 'user/accounts/registration.html', context)
            
            if User.objects.filter(phone=phone).exists():
                context = {
                    'pre_firstname': firstname,
                    'pre_lastname': lastname,
                    'pre_name': name,
                    'pre_email': email,
                }
                messages.error(request, 'Phone Number is already exists')
                return render(request, 'user/accounts/registration.html', context)


            if password1 != password2:
                context = {
                    'pre_firstname': firstname,
                    'pre_lastname': lastname,
                    'pre_name': name,
                    'pre_email': email,
                }
                messages.error(request, 'Passwords do not match')
                return render(request, 'user/accounts/registration.html', context)
            
           



            # If everything is valid, proceed with OTP generation and sending
            user_otp = random.randint(100000, 999999)
            print(user_otp,'daxoooooooo')
            usr = UserOTP.objects.create(
                first_name=firstname,
                last_name=lastname,
                username=name,
                email=email,
                phone=phone,
                password=password1,
                otp=user_otp
            )
            usr.save()

            # Send the OTP to the user's email
            mess = f'Hello\t{usr.username},\nYour OTP to verify your account for Street Wear is {user_otp}\nThanks!'
            send_mail(
                "Welcome to Streetwear! Verify your Email",
                mess,
                settings.EMAIL_HOST_USER,
                [usr.email],
                fail_silently=False
            )

            return render(request, 'user/accounts/registration.html', {'otp': True, 'usr': usr})
    else:
        return render(request, 'user/accounts/registration.html')



  

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def signout(request):
    logout(request)
    return redirect('home')

from django.contrib.auth.backends import ModelBackend  # Import the authentication backend


def mobile_login(request):
   
    if request.method=='POST':
        get_otp=request.POST.get('otp')
        if get_otp:
            get_phone=request.POST.get('phone')
            user=User.objects.get(phone=get_phone)
            if int(get_otp)==Mobile_Otp.objects.filter(user=user).last().otp:
                user.backend = f'{ModelBackend.__module__}.{ModelBackend.__qualname__}'
                login(request, user)
                Mobile_Otp.objects.filter(user=user).delete()
                return redirect('home')   
            else:
                messages.warning(request,'You Entered a wrong OTP!')
                return render(request,'user/accounts/mobile_login.html',{'otp':True,'user':user})  
        else:
        
            phone=request.POST['phone']
        
            if phone.strip()=='':
                messages.error(request,'field cannot empty!')
                return redirect('mobile_login')
        
    
            if not re.search(re.compile(r'(\+91)?(-)?\s*?(91)?\s*?(\d{3})-?\s*?(\d{3})-?\s*?(\d{4})'), phone):   
                messages.error(request,'phone number should only contain numeric!')  
                
                return render(request,'user/accounts/mobile_login.html')
                    
            if User.objects.filter(phone=phone):
                user=User.objects.get(phone=phone)
                user_otp=random.randint(100000,999999)
                Mobile_Otp.objects.create(user=user,otp=user_otp)
                c_phone = '+91' + phone
                mixins.send_otp_on_phone(c_phone,user_otp)
            
                return render (request,'user/accounts/mobile_login.html',{'otp':True,'user':user}) 
            else:
                messages.error(request,'phone  does not exist!')
                return render(request,'user/accounts/mobile_login.html')
    return render (request,'user/accounts/mobile_login.html') 


#----------------------------------------Admin authenication------------------------------------------

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def admin_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password=password)

        if user and user.is_superuser:
            login(request,user)
            return redirect('dashboard')
        
        messages.error(request,'Invalid username or Password.')
        return redirect('admin_login')
    
    return render  (request,'user/accounts/adminlogin.html')

    
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def admin_logout(request):
    logout(request)
    return redirect('admin_login')



def forgot_password(request):
    if request.method=='POST':
        get_otp=request.POST.get('otp')
        
        if get_otp:
            get_email=request.POST.get('email')
            user=User.objects.get(email=get_email)
            if not re.search(re.compile(r'^\d{6}$'), get_otp): 
                messages.error(request,'OTP should only contain numeric!')
                return render(request,'user/accounts/password_forgot.html',{'otp':True,'user':user}) 
            session_otp=request.session.get('otp')
            if int(get_otp) == session_otp:
                password1 = request.POST.get('password1')
                password2 = request.POST.get('password2')
                context ={
                                'pre_otp':get_otp,
                            }
                if password1.strip()==''or password2.strip()=='':
                    messages.error(request,'field cannot empty !')
                    return render(request,'user/accounts/password_forgot.html',{'otp':True,'user':user,'pre_otp':get_otp})
                
                elif password1 != password2:
                    messages.error(request,'Password does not match!')
                    return render(request,'user/accounts/password_forgot.html',{'otp':True,'user':user,'pre_otp':get_otp})
                    
                Pass = ValidatePassword(password1)
                if Pass is False:
                    messages.error(request,'Please enter Strong password!')
                    return render(request,'user/accounts/password_forgot.html',{'otp':True,'user':user,'pre_otp':get_otp})
                user.set_password(password1)
                user.save()
                del request.session['otp']
                messages.success(request,'Your password is changed!')
                return redirect('signin')
            else:
                messages.warning(request,'You Entered a wrong OTP!')
                return render(request,'user/accounts/password_forgot.html',{'otp':True,'user':user})  
        else:
            
            get_otp=request.POST.get('otp1')
            email=request.POST.get('user1')
            if get_otp:
                user=User.objects.get(email=email)
                messages.error(request,'field cannot empty!')
                return render(request,'user/accounts/password_forgot.html',{'otp':True,'user':user})
                
            else:   
                email=request.POST['email']
                
                if email.strip()=='':
                    messages.error(request,'field cannot empty!')
                    return render(request,'user/accounts/password_forgot.html')
                
                email_check=validateEmail(email)
                if email_check is False:
                    messages.error(request,'email not valid!')
                    return render(request,'user/accounts/password_forgot.html')
            
                if User.objects.filter(email=email):
                    user=User.objects.get(email=email)
                    user_otp=random.randint(100000,999999)
                    request.session['otp']=user_otp
                    message=f'Hello\t{user.first_name},\n Your OTP to verify your account for Coot is {user_otp}\n Thanks' 
                    send_mail(
                        "welcome to Coot Verify Email",
                        message,
                        settings.EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=False
                    )
                    return render (request,'user/accounts/password_forgot.html',{'otp':True,'user':user}) 
                else:
                    messages.error(request,'email does not exist!')
                    return render(request,'user/accounts/password_forgot.html')
    return render (request,'user/accounts/password_forgot.html')  