from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
# Create your views here.

def product_management(request):
    products = Product.objects.all()
    return render (request,'adminside/product/product_management.html',{'products':products})

def delete_product(request,prod_id):
    try:
        product = Product.objects.get(id=prod_id)
    except Product.DoesNotExist:
        return redirect ('product_management')
    if product.is_available:
        product.is_available = False
    else:
        product.is_available = True
    product.save()

    return redirect('product_management')

def add_product(request):
    if request.method == 'POST':
        name = request.POST['product_name']
        price = request.POST.get('product_price')
        image1 = request.FILES['image1']
        image2 = request.FILES['image2']
        image3 = request.FILES['image3']
        brand_id = request.POST['brand']
        description = request.POST['product_description']
        stock = request.POST['stock']
        category_id = request.POST['category']



        if Product.objects.filter(product_name=name).exists():
            messages.error(request,'Product name already exists')
            return redirect('product_management')
        if name == '' or price == '':
            messages.error(request,'Name or Price Fields are empty')
            return redirect('product_management')
        
        categoryid = Category.objects.get(id=category_id)
        brandid = Brand.objects.get(name =brand_id )


        product = Product(
            product_name = name,
            product_price = price,
            brand = brandid,
            category = categoryid,
            stock = stock,


        )



