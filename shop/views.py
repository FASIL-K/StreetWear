from django.shortcuts import render,redirect
from products.models import Product
from category.models import *
from products.models import *
# Create your views here.


def single(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except:
        return redirect('shop')
    context = {
        'product': product
    }
    return render(request, 'user/shop/single_page.html', context)
    


def shop(request):
    category = request.GET.get('category')
    brand = request.GET.get('brand')
    size = request.GET.get('size')
    sort = request.GET.get('sort')
    pricerange = request.GET.get('pricerange')
    if category:
         product =Product.objects.filter(is_available = True,category=category)
    elif brand:
        product =Product.objects.filter(is_available = True,brand=brand)
    elif size:
        product =Product.objects.filter(is_available = True,sizes=size)
    elif sort == 'atoz':
        product =Product.objects.filter(is_available = True).order_by('product_name')
    elif sort=='ztoa':
        product =Product.objects.filter(is_available = True).order_by('-product_name')
    elif sort=='ltoh':
        product =Product.objects.filter(is_available = True).order_by('product_price')
    elif sort=='htol':
        product =Product.objects.filter(is_available = True).order_by('-product_price')
    elif pricerange:
        price_ranges = price_range.objects.get(id=pricerange)
        product = Product.objects.filter(is_available=True, product_price__gte=price_ranges.low,product_price__lte=price_ranges.high)
        print(product,'sifandaxo')
    else:
        product =Product.objects.filter(is_available = True)


    categories = Category.objects.all()
    brands = Brand.objects.all()
    size =Size.objects.all()
    product_count = product.count()
    pricerange = price_range.objects.all()
    context ={
        'categories' : categories,
        'brands' : brands,
        'products': product,
        'size':size,
        'pricerange':pricerange,
        'product_count':product_count,
    }
    return render(request,'user\shop\shop.html',context)