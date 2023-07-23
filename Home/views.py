from django.shortcuts import render
from category.models import *
from products.models import *

# Create your views here.
def home(request):
    return render(request,'user\home\home.html')

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