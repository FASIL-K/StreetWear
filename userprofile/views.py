from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Address
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
import re
from django.forms import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from .models import Wallet

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='signin')
def userprofile(request):
    user = get_object_or_404(User, email=request.user.email)
    address = Address.objects.filter(user=request.user)
    context = {
        'user1': user,
        'address': address,
        'wallets': Wallet.objects.filter(user=request.user),

    }
    return render(request, 'user/accounts/profile.html', context)


def addaddress(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        country = request.POST.get('country')
        address = request.POST.get('address')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        state = request.POST.get('state')
        order_note = request.POST.get('ordernote')
        
        if request.user is None:
            return 
        if first_name.strip() == '' or last_name.strip() == '':
            messages.error(request, 'First name or Last name is empty!')
            return redirect('userprofile')
        if country.strip() =='':
            messages.error(request, 'Country is empty!')
            return redirect('userprofile')
        if city.strip() =='':
            messages.error(request, 'City is empty!')
            return redirect('userprofile')
        if address.strip() =='':
            messages.error(request, 'Address is empty!')
            return redirect('userprofile')
        if pincode.strip() =='':
            messages.error(request, 'Pincode is empty!')
            return redirect('userprofile')
        if phone.strip() =='':
            messages.error(request, 'Phone is empty!')
            return redirect('userprofile')
        if email.strip() =='':
            messages.error(request, 'Email is empty!')
            return redirect('userprofile')
        if state.strip() =='':
            messages.error(request, 'State is empty!')
            return redirect('userprofile')
        if not re.search(re.compile(r'^\d{6}$'),pincode ):  
            messages.error(request,'should only 6 contain numeric!')   
            return redirect('userprofile')
        if not re.search(re.compile(r'(\+91)?(-)?\s*?(91)?\s*?(\d{3})-?\s*?(\d{3})-?\s*?(\d{4})'),phone): 
            messages.error(request,'Enter valid phonenumber!')
            return redirect('userprofile')
        phonenumber_checking=len(phone)
        if not  phonenumber_checking==10:
            messages.error(request,'phonenumber should be must contain 10digits!')  
            return redirect('userprofile')
        email_check=validateemail(email)
        if email_check is False:
            messages.error(request,'email not valid!')
            return redirect('userprofile')
        adrs = Address()
        adrs.user = request.user
        adrs.first_name = first_name
        adrs.last_name = last_name
        adrs.country = country
        adrs.address = address
        adrs.city = city
        adrs.pincode = pincode
        adrs.phone = phone
        adrs.email = email
        adrs.state = state
        adrs.order_note = order_note
        adrs.save()

        return redirect('userprofile')
    

# edit Userprofiles
def editprofiles(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        # Validation
        if username == '':
            messages.error(request, 'Username is empty')
            return redirect('userprofile')
        if first_name == '' or last_name == '':
            messages.error(request, 'First or Lastname is empty')
            return redirect('userprofile')

        try:
            user = User.objects.get(username=request.user)
            print(user)
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except ObjectDoesNotExist:
            messages.error(request, 'User does not exist')
        return redirect('userprofile')
    
# Change Password 
def changepassword(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')
#  Validation
        if new_password != confirm_new_password:
            messages.error(request,'Password did not match')
            return redirect('userprofile')
        user = User.objects.get(username = request.user)
        if check_password(old_password, user.password):
            user.set_password(new_password)
            user.save()

            update_session_auth_hash(request, user)

            messages.success(request, 'Password updated successfully')
            return redirect('userprofile')
        else:
            messages.error(request, 'Invalid old password')
            return redirect('userprofile')
    return redirect('userprofile')


# delete Address
def deleteaddress(request,delete_id):
    address = Address.objects.get(id = delete_id)
    address.delete()
    return redirect('userprofile')


def validateemail(email):
    try:
        validate_email(email)
        return True
    except ValidationError: 
        return False
    
def validatepassword(new_password):
    try:
        validate_password(new_password)
        return True
    except  ValidationError:
        return  False