from django.shortcuts import render
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from cart.models import Cart
from userprofile.models import Address
from django.contrib.auth.models import User
from django.contrib import messages
from products.models import *
from checkout.models import Order, OrderItem
from django.shortcuts import render, redirect
import random
# Create your views here.
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def checkout(request):
    cartitems = Cart.objects.filter(user= request.user)
    total_price = 0
    grand_total = 0
    tax = 0
    for item in cartitems:
        total_price = total_price + item.product.product_price * item.product_qty
        tax = total_price * 0.18
        grand_total = total_price + tax
    address = Address.objects.filter(user = request.user)
    context = {
        'cartitems' : cartitems,
        'total_price' :total_price,
        'grand_total' : grand_total,
        'address' : address,

    }

    return render(request, 'user/checkout/checkout.html',context)

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def placeorder(request):
    if request.method == 'POST':
        neworder = Order()
        neworder.user = request.user
        address_id = request.POST.get('address')
        if address_id is None:
            messages.error(request, 'Address fields is mandatory!')
            return redirect('checkout')
        address = Address.objects.get(id=address_id)
        neworder.address = address
        payment_method = request.POST.get('payment_method')
        if payment_method is None:
            messages.error(request,'Please select any Payment option')
            return redirect('checkout')
        neworder.payment_mode =payment_method
        neworder.payment_id = request.POST.get('payment_id')
        cart = Cart.objects.filter(user=request.user)
        cart_total_price = 0
        tax = 0
        for item in cart:
           
            cart_total_price += item.product.product_price * item.product_qty
            tax = cart_total_price * 0.18
            cart_total_price +=tax
            
        neworder.total_price = cart_total_price
        trackno = random.randint(1111111, 9999999)
        while Order.objects.filter(tracking_no=trackno).exists():
            trackno = random.randint(1111111, 9999999)
        neworder.tracking_no = trackno
        neworder.save()

        neworderitems = Cart.objects.filter(user=request.user)
        for item in neworderitems:
            size = Size.objects.get(id=item.selected_size)
            OrderItem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.product_price,
                quantity=item.product_qty,
                selected_size = size,
            )

            # To decrease the product quantity from available stock
            prod = Product.objects.filter(id=item.product.id).first()
            prod.stock = prod.stock - item.product_qty
            prod.save()
        Cart.objects.filter(user=request.user).delete()
    return redirect('checkout')




def addcheckoutaddr(request):
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
            return redirect('checkout')
        if country.strip() =='':
            messages.error(request, 'Country is empty!')
            return redirect('checkout')
        if city.strip() =='':
            messages.error(request, 'City is empty!')
            return redirect('checkout')
        if address.strip() =='':
            messages.error(request, 'Address is empty!')
            return redirect('checkout')
        if pincode.strip() =='':
            messages.error(request, 'Pincode is empty!')
            return redirect('checkout')
        if phone.strip() =='':
            messages.error(request, 'Phone is empty!')
            return redirect('checkout')
        if email.strip() =='':
            messages.error(request, 'Email is empty!')
            return redirect('checkout')
        if state.strip() =='':
            messages.error(request, 'State is empty!')
            return redirect('checkout')
        
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

    return redirect('checkout')

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def deleteaddresscheckout(requst,delete_id):
    address = Address.objects.filter(id=delete_id)
    address.delete()
    return redirect('placeorder')