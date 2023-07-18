from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .models import Category,Brand
from django.contrib import messages


# Create your views here.


def category_management(request):
    categories = Category.objects.all()
    return render (request,'adminside/category/category_management.html',{'categories':categories})

def add_category(request):
    if request.method == 'POST' :
        name = request.POST['category_name']
        description = request.POST['category_discrption']
        
        if name.strip() == '' or description.strip()=='':
            messages.error(request,'Fields Cannot empty.')
            return HttpResponseRedirect(request.path_info) 
        if Category.objects.filter(name = name).exists():
            messages.error(request,'Category name is exists.')
            return HttpResponseRedirect(request.path_info)
        Category.objects.create(name=name,description=description)
        messages.success(request,'New Category Created successfully')

    return redirect(category_management)

def edit_category(request,category_id):
    category =Category.objects.get(id=category_id)
    if request.method == 'POST':
        name = request.POST['category_name']
        description = request.POST['description']


        if  Category.objects.filter(name=name).exists():

            messages.warning(request,'Category name already exists. ')
            return HttpResponseRedirect(request.path_info)
        
        category.name = name
        category.description = description
        category.save()
        messages.success(request,'Category edited Successfully')

    return render(request,'adminside/category/edit_category.html',{'category':category})


def delete_category(request,category_id):
    category = Category.objects.get(id=category_id)
    category_name = str(category)
    category.delete()
    messages.success(request,f'{category_name} category deleted.' )
    return redirect(category_management)


#---------------------------Brand management-----------------------------------------

def brand_management(request):
    brands=Brand.objects.all().order_by('id')
    return render(request,'adminside/brand/brand_management.html',{'brands':brands})

def add_brand(request):
    if request.method == 'POST':
        name = request.POST['brand_name']

        if Brand.objects.filter(name=name).exists():
            messages.error(request,'Braname is already exists')
            return HttpResponseRedirect(request.path_info)
        
        if name.strip()=='':
            messages.error(request,'Field cannot empty')
            return HttpResponseRedirect(request.path_info)
        
        Brand.objects.create(name=name)
        messages.success(request,'New Brand added Successfully')
        return HttpResponseRedirect(request.path_info)
    
    return redirect('brand_management')

def edit_brand(request,brand_id):
    brand = Brand.objects.get(id=brand_id)
    if request.method =='POST':
        name = request.POST['brand_name']

        if Brand.objects.filter(name=name).exists():
            messages.warning(request,'Brand name was already exists')
            return HttpResponseRedirect(request.path_info)
        brand.name = name 
        brand.save()
        messages.success(request,'brand edited Successfully')
        return redirect('edit_brand',brand_id=brand.id)
    
    return render(request,'adminside/brand/edit_brand.html',{'brand':brand})

   

def delete_brand(request,brand_id):
    brand = Brand.objects.get(id=brand_id)
    brandname=str(brand)
    brand.delete()
    messages.success(request,f'{brandname} brand deletes successfully')
    return redirect(brand_management)





