from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .models import Wishlist
from products.models import Product, Size
from django.http.response import JsonResponse




# Create your views here.
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def wishlist(request):
    wishlist = Wishlist.objects.filter(user = request.user)
    context = {
        'wishlist' : wishlist,
    }
    return render(request,'user/wishlist/wishlist.html',context)


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def add_wishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = request.POST.get('prod_id')
            # size_id =  request.POST.get('size_id')
            print(prod_id,'daxoooooooooooooooooooo')
            product_check = Product.objects.get(id = prod_id)
            if(product_check):
                if(Wishlist.objects.filter(user = request.user, product = product_check)):
                    return JsonResponse({'status' : "Product already in wishlist"})
                else:
                    Wishlist.objects.create(user=request.user, product = product_check)
                    return JsonResponse({'status' : "Product Added to in wishlist"})
            else:
                JsonResponse({'status' : "No such product"})

        else:
            return JsonResponse({'status' : "Login to continue"})
    else:
        return JsonResponse('something went wrong, reload page',safe=False)


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def deletewishlist(request):
    if request.method == 'POST':
        product_id = int(request.POST.get('prod_id'))
        wishlist = Wishlist.objects.filter(user=request.user, product_id=product_id)
        if wishlist.exists():
            wishlist.delete()
    return redirect('wishlist')
