from django.shortcuts import render,redirect
from .models import Banner
from django.contrib import messages
from category.models import Category

# Create your views here.


def banner(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    dict_banner={
        'banner' : Banner.objects.all(),
        'category':Category.objects.all(),
        
    }
    return render(request,'adminside/banner/banner.html',dict_banner)


def createbanner(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    
    if request.method == 'POST':
        name = request.POST['banner_name']
        description = request.POST['banner_discription']
        image = request.FILES.get('image', None)
        category_id = request.POST.get('category', None)  # Get the selected category ID from the form
        
        # Validation
        if name.strip() == '':
            messages.error(request, "Name Field empty")
            return redirect('banner')

        if not image:
            messages.error(request, "Image not uploaded")
            return redirect('banner')

        if not category_id:
            messages.error(request, "Category not selected")
            return redirect('banner')

        try:
            category_instance = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            messages.error(request, "Invalid category selected")
            return redirect('banner')

        ban = Banner(
            banners_image=image,
            banner_name=name,
            banner_discription=description,
            category=category_instance,  # Associate with the selected category
        )
        ban.save()
        
    return redirect('banner')


#  Edit Banner
def editbanner(request,banner_id):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    if request.method == 'POST':
        name = request.POST['banner_name']
        description = request.POST['banner_discription']
        categories = request.POST['categories']
# validation
    if name.strip() == '':
        messages.error(request, "Name Field empty")
        return redirect('banner')

    try:
        ban = Banner.objects.get(id=banner_id)
        image = request.FILES['image']
        ban.banners_image = image
        ban.save()
    except:
        pass 
    ban = Banner.objects.get(id=banner_id)
    ban.banner_name = name
    ban.banner_discription = description
    ban.save()      
    return redirect('banner')

# Delete Banner
def deletebanner(request,banner_id):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    ban = Banner.objects.get(id = banner_id)
    ban.delete()
    return redirect('banner')
