
from django.shortcuts import render,redirect
from .models import Coupon,CouponUsage
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# Create your views here.
@login_required(login_url='admin_login')
def coupons(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    
    coupons=Coupon.objects.all()
    context={
        'coupons':coupons
    }
    return render(request,'adminside/coupon/coupon.html',context)


def addcoupons(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    if request.method=='POST':
        coupon = request.POST.get('coupon')
        print(coupon,'daxoooooooooooo')
        coupon_code = request.POST.get('coupon_code')
        discount = request.POST.get('discount')
        min_price = request.POST.get('min_price')
        valid_from = request.POST.get('valid_from')
        valid_to = request.POST.get('valid_to')

        try:
            is_active = request.POST.get('is_active',False)
            if is_active == 'on':
                is_active=True
            else:
                is_active = False
        except:
            is_active = False
        
        if Coupon.objects.filter(coupon=coupon).exists():
            messages.error(request,'coupon code already exists')
            return redirect ('coupons')
        if Coupon.objects.filter(coupon_code=coupon_code).exists():
            messages.error(request,'coupon code already exists')
            return redirect('coupons')
        
        coupon =Coupon(
            coupon=coupon,
            coupon_code=coupon_code,
            discount=discount,
            min_price=min_price,
            valid_from=valid_from,
            valid_to=valid_to,
            is_active=is_active
        )
        coupon.save()
        return redirect('coupons')
    

def apply_coupon(request):
    if request.method =="POST":
        coupon_code = request.POST.get('coupon_code')
        grand_total = float(request.POST.get('grand_total',0))

        if coupon_code.strip()== '':
            return JsonResponse({'status':'No Coupon Applied'})
        
        try:
            coupon=Coupon.objects.get(coupon_code=coupon_code,is_active=True)
        except:
            return JsonResponse({'status':'Coupon does not exist'})
        
        if CouponUsage.objects.filter(user=request.user).exists():
            return JsonResponse ({'status':'Coupon already used'})
        
        if grand_total > coupon.min_price:
            coupon_discount = coupon.discount
            grand_Total = grand_total-(grand_total * (coupon.discount / 100))
            discount = coupon.discount/100 * grand_Total
            usercoupon = CouponUsage.objects.create(user=request.user,coupon=coupon,used=True,total_price=grand_Total)
            usercoupon.save()
            return JsonResponse({
                'status': 'Coupon added successfully',
                'coupon_discount': coupon_discount,
                'grand_Total': grand_Total,
                'discount':discount
             })
        else:
            return JsonResponse({'status':'You are not eligible for this coupon'})
    return JsonResponse({'status':'Invalid request'})


def remove_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')

        if coupon_code.strip() == '':
            return JsonResponse({'status': 'Field is blank'})

        if coupon_code == 'No Coupon Applied':
            return JsonResponse({'status': 'No Coupon Applied'})

        try:
            coupon = get_object_or_404(Coupon, coupon_code=coupon_code, is_active=True)
        except Coupon.DoesNotExist:
            return JsonResponse({'status': 'Coupon does not exist'})

        existing_coupon_usage = CouponUsage.objects.filter(user=request.user, coupon=coupon)
        if existing_coupon_usage.exists():
            existing_coupon_usage = existing_coupon_usage.first()
            grand_total = float(request.POST.get('grand_total', 0))
            # Add the discount of the existing coupon back to the grand_total
            grand_total += (grand_total * (existing_coupon_usage.coupon.discount / 100))
            existing_coupon_usage.delete()

            return JsonResponse({
                'status': 'Coupon removed successfully',
                'grand_total': grand_total,
            })
        else:
            return JsonResponse({'status': 'Coupon is not applied'})

    return JsonResponse({'status': 'Invalid request'})