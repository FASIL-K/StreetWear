from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Address
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def userprofile(request):
    return render(request,'user/accounts/profile.html')


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
            return redirect('profile')
        if country.strip() =='':
            messages.error(request, 'Country is empty!')
            return redirect('profile')
        if city.strip() =='':
            messages.error(request, 'City is empty!')
            return redirect('profile')
        if address.strip() =='':
            messages.error(request, 'Address is empty!')
            return redirect('profile')
        if pincode.strip() =='':
            messages.error(request, 'Pincode is empty!')
            return redirect('profile')
        if phone.strip() =='':
            messages.error(request, 'Phone is empty!')
            return redirect('profile')
        if email.strip() =='':
            messages.error(request, 'Email is empty!')
            return redirect('profile')
        if state.strip() =='':
            messages.error(request, 'State is empty!')
            return redirect('profile')
        
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