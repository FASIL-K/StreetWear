from django.shortcuts import render
from category.models import *

# Create your views here.
def home(request):
    return render(request,'user\home\home.html')

def shop(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()
    context ={
        'categories' : categories,
        'brands' : brands
    }
    return render(request,'user\shop\shop.html',context)