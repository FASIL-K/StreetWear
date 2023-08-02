from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
import os
from django.conf import settings
# Create your views here.
@staff_member_required(login_url='admin_login')
def product_management(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    products = Product.objects.all()
    available_sizes = Size.objects.all()
    print(available_sizes) 
    context={
        'products' : products,
        'category' : Category.objects.all(),
        'brand' : Brand.objects.all(),
        'available_sizes': available_sizes,

    }
    return render (request,'adminside/product/product_management.html',context)

@staff_member_required(login_url='admin_login')
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

@staff_member_required(login_url='admin_login')
def add_product(request):
    if not request.user.is_superuser:
        return redirect('admin_login')
    
    # Fetch available sizes
    available_sizes = Size.objects.all()

    if request.method == 'POST':
        name = request.POST['product_name']
        price = request.POST.get('product_price')
        image1 = request.FILES.get('image1', None)
        image2 = request.FILES.get('image2', None)
        image3 = request.FILES.get('image3', None)
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
        if Product.objects.filter(product_name=name).exists():
            messages.error(request, 'Product name already exists')
            return redirect('product_management')

        try:
            is_availables = request.POST.get('checkbox', False)
            if is_availables == 'on':
                is_availables = True
            else:
                is_availables = False
        except:
            is_availables = False

        categoryid = Category.objects.get(id=category_id)
        brandid = Brand.objects.get(name=brand_id)

        # Save the product without the sizes first
        product = Product(
            product_name=name,
            product_price=price,
            brand=brandid,
            category=categoryid,
            stock=stock,
            product_description=description,
            is_available=is_availables,
            image1=image1,
            image2=image2,
            image3=image3,
        )
        product.save()

        # Fetch selected size IDs from the form
        selected_size_ids = request.POST.getlist('sizes')

        # Fetch available sizes based on the selected IDs
        selected_sizes = Size.objects.filter(id__in=selected_size_ids)

        # Add the selected sizes to the product's M2M field
        product.sizes.set(selected_sizes)

        return redirect('product_management')

    context = {
        'available_sizes': available_sizes,
        'category': Category.objects.all(),
        'brand': Brand.objects.all(),
    }

    return render(request, 'adminside/product/product_management.html', context)
    


def delete_image(file_path):
    """Helper function to delete an image file."""
    if os.path.exists(file_path):
        os.remove(file_path)

def replace_image(product, image_field, new_image, delete_image_flag=False):
    """Helper function to replace an existing image or delete it if delete_image_flag is True."""
    if delete_image_flag:
        # Delete the old image
        if getattr(product, image_field):
            delete_image(getattr(product, image_field).path)
        # Set the image field to None
        setattr(product, image_field, None)
    elif new_image:
        # Delete the old image
        if getattr(product, image_field):
            delete_image(getattr(product, image_field).path)
        # Set the new image
        setattr(product, image_field, new_image)

def edit_product(request, editproduct_id):
    if not request.user.is_superuser:
        return redirect('admin_login')

    try:
        product = Product.objects.get(id=editproduct_id)
    except Product.DoesNotExist:
        return redirect('product_management')

    if request.method == "POST":
        pname = request.POST.get('product_name')
        pprice = request.POST.get('product_price')
        pdescription = request.POST.get('product_description')
        brandname = request.POST.get('brand')
        stock = request.POST.get('stock')
        category_id = request.POST.get('category')
        is_availables = request.POST.get('checkbox', False) == 'on'

        replace_image(product, 'image1', request.FILES.get('image1'), request.POST.get('delete_image1') == 'on')
        replace_image(product, 'image2', request.FILES.get('image2'), request.POST.get('delete_image2') == 'on')
        replace_image(product, 'image3', request.FILES.get('image3'), request.POST.get('delete_image3') == 'on')

        product.product_name = pname
        product.product_price = pprice
        product.product_description = pdescription
        product.is_available = is_availables
        product.stock = stock


        brand_obj = Brand.objects.get(name=brandname)
        category_obj = Category.objects.get(id=category_id)

        product.brand = brand_obj
        product.category = category_obj

        product.save()

        # Retrieve the selected sizes from the request
        selected_sizes_ids = request.POST.getlist('sizes')

        # Clear the existing sizes for the product
        product.sizes.clear()

        # Add the selected sizes to the product
        for size_id in selected_sizes_ids:
            size = Size.objects.get(id=size_id)
            product.sizes.add(size)

        return redirect('product_management')

    context = {
        'product': product,
        'category': Category.objects.all(),
        'brand': Brand.objects.all(),
        'available_sizes': Size.objects.all(),
    }

    return render(request, 'adminside/product/product_management.html', context)


