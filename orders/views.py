from django.shortcuts import render
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from checkout.models import Order, OrderItem
from django.contrib import messages
from userprofile.models import Address
from django.contrib.admin.views.decorators import staff_member_required
from django.http.response import JsonResponse
from products.models import Size,Product
from .models import *
from userprofile.models import Wallet
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator



from django.shortcuts import render, redirect
# Create your views here.
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def orders(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')
    orderitems = OrderItem.objects.filter(order__in=orders).order_by('-order__created_at')

    context = {
        'orders': orders,
        'orderitems': orderitems,
    }
    return render(request, 'user/orders/orders.html', context)


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def vieworderdetail(request,orderitem_id):
    try:
        order_item = OrderItem.objects.filter(order__tracking_no=orderitem_id)
        order = Order.objects.get(tracking_no = orderitem_id)
    except Order.DoesNotExist:
        messages.error(request, "The specified OrderItem does not exist.")
        return redirect('orders')
        
    address = int(order.address.id)
    context = {
        'order' : order,
        'address': Address.objects.get(id=address),
        'order_item' : order_item,
    }
    return render(request, 'user/orders/vieworder.html',context)




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@staff_member_required(login_url='admin_login')
def order_management(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    orders = Order.objects.all().order_by('-created_at')
    orderitems = OrderItem.objects.filter(order__in=orders).order_by('-order__updated_at')
    context = {
        'orders': orders,
        'orderitems' : orderitems,
    }
    return render(request,'adminside/order/order_management.html',context) 


def orderdetails_admin(requset,track_id):
    try:
        order_item = OrderItem.objects.filter(order__tracking_no=track_id)
        order = Order.objects.get(tracking_no = track_id)
    except Order.DoesNotExist:
        messages.error(requset,"The specified OrderItem does not exist.")
        return redirect('orderdetails')
    address = int(order.address.id)
    
    context={
        'order' : order,
        'address' : Address.objects.get(id=address),
        'order_item' : order_item,
    }

    return render(requset,'adminside/order/ordersdetails.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@staff_member_required(login_url='admin_login')
def changestatus(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    orderitem_id = request.POST.get('orderitem_id')
    order_status = request.POST.get('order_status')

    orderitems = OrderItem.objects.get(id = orderitem_id)
    orderitems.status = order_status

    orderitems.save()
    return JsonResponse({'status': "Updated"+ str(order_status)+"successfuly"})

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def ordercancel(request):
    order_id = int(request.POST.get('order_id'))
    orderitem_id = request.POST.get('orderitem_id')
    orderitem = OrderItem.objects.filter(id=orderitem_id).first()
    order = Order.objects.filter(id=order_id).first()

    qty = orderitem.quantity
    pid = orderitem.selected_size.id
    product = Product.objects.filter(id=pid).first()

    product.stock = product.stock + qty
    product.save()

    orderitem.quantity = 0
    orderitem.status = 'Cancelled'
    orderitem.save()

    # Refund money to wallet if payment mode is wallet or razorpay
    if order.payment_mode in ['wallet', 'razorpay']:
        wallet = Wallet.objects.get_or_create(user=request.user)[0]
        wallet.wallet += order.total_price
        wallet.save()

    return redirect('orders')


def orderreturn(request,return_id):
    if request.method == 'POST':
        options = request.POST.get('options')
        reason = request.POST.get('reason')

        if options.strip() == '':
            messages.error(request,"enter valid Options")
            return redirect('vieworderdetail')
        
        try:
            orderitem_id = OrderItem.objects.get(id=return_id)
        except :
            return redirect('orders')
        
        qty = orderitem_id.quantity
        pid = orderitem_id.product.id
        order_id = Order.objects.get(id = orderitem_id.order.id)
        tracking_id = order_id.tracking_no
        product = Product.objects.filter(id=pid).first()
        product.stock = product.stock + qty
        product.save()
        orderitem_id.status = 'Return'
        total_p = orderitem_id.price
        orderitem_id.save()
        returnorder = Orderreturn.objects.create(user = request.user, order = order_id, options=options, reason=reason)
        try :
            wallet = Wallet.objects.get(user=request.user)
            wallet.wallet += total_p
            wallet.save()
        except Wallet.DoesNotExist:
            wallet = Wallet.objects.create(user=request.user,wallet=total_p)
        orderitem_id.quantity = 0
        orderitem_id.price = 0
        orderitem_id.save()
        return redirect('vieworderdetail',tracking_id)







