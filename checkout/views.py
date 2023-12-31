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
import string
import re
from django.forms import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from coupon.models import Coupon,CouponUsage
from userprofile.models import Wallet
from django.http import HttpResponse
from django.conf import settings
import os
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage

# Create your views here.
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def checkout(request):
    cartitems = Cart.objects.filter(user= request.user)
    total_price = 0
    grand_total = 0
    max_discount = 0
    for item in cartitems:
        product_price = item.product.product_price
        product_offer = item.product.offer

        if product_offer is None:
            total_price += product_price * item.product_qty
        else:
            if product_offer:
                max_discount = product_offer.discount_amount
                    
                discount = (max_discount / 100) * product_price
                discounted_price = product_price - discount

                total_price += discounted_price * item.product_qty

        
    coupons = Coupon.objects.filter(is_active=True)
    applied_coupon = None
    grand_total = total_price 

    if request.method == 'POST':
        coupon_code =request.POST.get('coupon_code')
        if coupon_code:
            try:
                applied_coupon = Coupon.objects.get(coupon_code=coupon_code,is_active=True)
                grand_total= total_price-(total_price * (applied_coupon.discount / 100))
            except:
                pass



    address = Address.objects.filter(user = request.user)
    context = {
        'cartitems' : cartitems,
        'total_price' :total_price,
        'grand_total' : grand_total,
        'address' : address,
        'coupons': coupons,
        'CouponUsage': CouponUsage.objects.filter(user=request.user).last(),

    }

    return render(request, 'user/checkout/checkout.html',context)

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def placeorder(request):
    if request.method == 'POST':
        max_discount = 0
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
            messages.error(request, 'Please select any Payment option')
            return redirect('checkout')

        neworder.payment_mode = payment_method
        neworder.payment_id = request.POST.get('payment_id')
        cart = Cart.objects.filter(user=request.user)
        cart_total_price = 0
        
        
        for item in cart:
            product_price = item.product.product_price
            product_offer = item.product.offer
            if product_offer is None:
                cart_total_price += product_price * item.product_qty
            else:
                if product_offer:
                    max_discount = product_offer.discount_amount
            
                    discount = (max_discount / 100) * product_price
                    discounted_price = product_price - discount
                    cart_total_price += discounted_price * item.product_qty

        neworder.total_price = cart_total_price
        payment_mode = request.POST.get('payment_method')
        if payment_mode == 'wallet':
            try:
                wallet = Wallet.objects.get(user=request.user)
            except Wallet.DoesNotExist:
                wallet = Wallet.objects.create(user=request.user, wallet=0)  # Create a new Wallet object if it doesn't exist
                
            if wallet.wallet >= cart_total_price:
                wallet.wallet -= cart_total_price
                wallet.save()
            else:
                return JsonResponse({'status': "Your wallet amount is very low"})
            

        user=request.user
        coupon = CouponUsage.objects.filter(user=user,used=True).first()
        if coupon:
            # Calculate the discounted price if a coupon is applied
            discount = cart_total_price * (coupon.coupon.discount / 100)
            cart_total_price -= discount
            
        neworder.total_price = cart_total_price

        trackno = random.randint(1111111, 9999999)
        while Order.objects.filter(tracking_no=trackno).exists():
            trackno = random.randint(1111111, 9999999)
        neworder.tracking_no = trackno

        neworder.payment_id = generate_random_payment_id(10)
        while Order.objects.filter(payment_id=neworder.payment_id).exists():
            neworder.payment_id = generate_random_payment_id(10)

        neworder.save()


        
        

        neworderitems = Cart.objects.filter(user=request.user)
        for item in neworderitems:
            size = Size.objects.get(id=item.selected_size)
            OrderItem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.product_price,
                quantity=item.product_qty,
                selected_size=size,
            )

            # To decrease the product quantity from available stock
            prod = Product.objects.filter(id=item.product.id).first()
            prod.stock = prod.stock - item.product_qty
            prod.save()
            Cart.objects.filter(user=request.user).delete()
        
        payment_mode = request.POST.get('payment_method')
        if payment_mode == 'wallet':
            Cart.objects.filter(user=request.user).delete()
            return JsonResponse({'status': 'Your order has been placed successfully'})
        elif payment_mode == 'cod':
            Cart.objects.filter(user=request.user).delete()
            return JsonResponse({'status': 'Your order has been placed successfully'})
        return JsonResponse({'status': 'Your order has been placed successfully'})

        

        # Call a function to generate invoice PDF (implement this function separately)
    

        # Cart.objects.filter(user=request.user).delete()
    generate_invoice_pdf(request,neworder.id)

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
        if not re.search(re.compile(r'^\d{6}$'),pincode ):  
            messages.error(request,'should only 6 contain numeric!')   
            return redirect('checkout')
        if not re.search(re.compile(r'(\+91)?(-)?\s*?(91)?\s*?(\d{3})-?\s*?(\d{3})-?\s*?(\d{4})'),phone): 
            messages.error(request,'Enter valid phonenumber!')
            return redirect('checkout')
        phonenumber_checking=len(phone)
        if not  phonenumber_checking==10:
            messages.error(request,'phonenumber should be must contain 10digits!')  
            return redirect('checkout')
        email_check=validateemail(email)
        if email_check is False:
            messages.error(request,'email not valid!')
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


def generate_random_payment_id(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def razarypaycheck(request):
    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart:
        total_price = total_price + item.product.product_price * item.product_qty
        
        
    
    return JsonResponse({'total_price': total_price})

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
    


def generate_invoice_pdf(request,order_id):

    try:
        order = Order.objects.get(id=order_id)  
        order_items = OrderItem.objects.filter(order=order)
        
    except Order.DoesNotExist:
        # Handle the case if the order does not exist
        return HttpResponse("Order not found", status=404)

    # Render the XHTML template with dynamic data
    context = {
        'order': order,
        'order_items': order_items,
    }
    rendered_template = render_to_string('user/orders/invoice.html', context)

    # Convert the XHTML content to PDF
    pdf_file = os.path.join(settings.BASE_DIR, 'invoice.pdf')
    with open(pdf_file, 'wb') as pdf:
        pisa.CreatePDF(rendered_template, dest=pdf)

    # Send the email with both the PDF attachment and the order confirmation
    subject = "Welcome to Street Wear, Your Order is Placed!!!"
    message = f'''
        Your order has been placed successfully.
        Hello {order.user.username},
        Your Order has been placed successfully.
        Thank you for choosing Street Wear!
        Payment mode: {order.payment_mode}
        Your Payment ID is {order.payment_id}
        Your Order Tracking ID: {order.tracking_no}
    '''
    from_email = settings.EMAIL_HOST_USER
    to_email = [order.user.email]

    email = EmailMessage(subject, message, from_email, to_email)
    email.attach_file(pdf_file)  # Attach the PDF to the email
    email.send()

    # Delete the temporary PDF file
    os.remove(pdf_file)
    return redirect('placeorder')