from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import cache_control
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# verification email
from .models import UserOTP
from django.contrib import auth
from django.core.mail import send_mail
from django.conf import settings
import random
import re
from django.core.exceptions import ValidationError

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        print(user)
        if user is not None:
            login(request,user)
            return redirect('home')

    return render(request, 'user/accounts/login.html')

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

    if request.method=='POST':
        get_otp=request.POST.get('otp')
        if get_otp:
            get_email=request.POST.get('email')
            if int(get_otp)==UserOTP.objects.filter(email=get_email).last().otp:
                userotp = UserOTP.objects.get(email=get_email)
                user = User.objects.create_user(username=userotp.username,first_name=userotp.first_name,last_name=userotp.last_name,email=userotp.email,password=userotp.password)
                user.save()
                auth.login(request,user)
                # messages.success(request,f'Account is created for {usr.email}')
                UserOTP.objects.filter(email=get_email).delete()
                return redirect('home')
            else:
                messages.warning(request,f'You Entered a wrong OTP')
                return render(request,'user/accounts/registration.html',{'otp':True,'usr':usr})
            
        # User rigistration validation
        else:
            firstname = request.POST['firstname']   
            lastname = request.POST['lastname']  
            name = request.POST['name']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            # null values checking
            check = [name,email,password1,password2]
            for values in check:
                if values == '':
                    context ={
                        'pre_firstname' :firstname,
                        'pre_lastname' :lastname,
                        'pre_name':name,
                        'pre_email':email,
                    }
                    messages.info(request,'some fields are empty')
                    return render(request,'user/accounts/registration.html',context)
                else:
                    pass
            
            result = validate_name(name)
            if result is not False:
                context ={
                        'pre_firstname' :firstname,
                        'pre_lastname' :lastname,
                        'pre_name':name,
                        'pre_email':email,
                    }
                messages.info(request,result)
                return render(request,'user/accounts/registration.html',context)
            else:
                pass

            result = validateEmail(email)
            if result is False:
                context ={
                        'pre_firstname' :firstname,
                        'pre_lastname' :lastname,
                        'pre_name':name,
                        'pre_email':email,
                    }
                messages.info(request,'Enter valid email')
                return render(request,'user/accounts/registration.html',context)
            else:
                pass
            
            Pass = ValidatePassword(password1)
            if Pass is False:
                context ={
                        'pre_firstname' :firstname,
                        'pre_lastname' :lastname,
                        'pre_name':name,
                        'pre_email':email,
                    }
                messages.info(request,'Enter Strong Password')
                return render(request,'user/accounts/registration.html',context)
            else:
                pass
            if password1 == password2:
          
                if email:
                    if UserOTP.objects.filter(email=email).exists():
                        exuser = UserOTP.objects.get(email=email)
                        exuser.delete()
                    
                    user_otp=random.randint(100000,999999)
                    usr = UserOTP.objects.create(first_name=firstname, last_name=lastname, username=name,email=email,password=password1,otp=user_otp)
                    usr.save()
                    mess=f'Hello\t{usr.username},\nYour OTP to verify your account for Street Wear is {user_otp}\nThanks!'
                    send_mail(
                            "welcome to Streetwear Verify your Email",
                            mess,
                            settings.EMAIL_HOST_USER,
                            [usr.email],
                            fail_silently=False
                        )
                    return render(request,'user/accounts/registration.html',{'otp':True,'usr':usr})
                else:
                    context ={
                        'pre_firstname' :firstname,
                        'pre_lastname' :lastname,
                        'pre_name':name,
                        'pre_email':email,
                    }
                    messages.error(request,'Email already exist')
                    return render(request,'user/accounts/registration.html',context)
            else:
                context ={
                        'pre_firstname' :firstname,
                        'pre_lastname' :lastname,
                        'pre_name':name,
                        'pre_email':email,
                    }
                messages.error(request,'password mismatch')
                return render(request,'user/accounts/registration.html',context)
    else:      
        return render(request,'user/accounts/registration.html')


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def profile(request):
    return render(request,'user/accounts/profile.html')
  

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def signout(request):
    logout(request)
    return redirect('home')


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
