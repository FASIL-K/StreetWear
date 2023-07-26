from django.shortcuts import render
from products.models import Product
from category.models import *
from products.models import *
# Create your views here.


def single(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {
        'product': product
    }
    return render(request, 'user/shop/single_page.html', context)
    


def shop(request):
    categories = Category.objects.all()
    product =Product.objects.filter(is_available = True)
    brands = Brand.objects.all()
    context ={
        'categories' : categories,
        'brands' : brands,
        'products': product,
    }
    return render(request,'user\shop\shop.html',context)