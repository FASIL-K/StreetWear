from django.shortcuts import render
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from checkout.models import Order, OrderItem
from django.contrib import messages
from userprofile.models import Address

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
    cotext = {
        'order' : order,
        'address': Address.objects.get(id=address),
        'order_item' : order_item,
    }
    return render(request, 'user/orders/vieworder.html',cotext)