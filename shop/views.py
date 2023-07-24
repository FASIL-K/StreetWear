from django.shortcuts import render
from products.models import Product

# Create your views here.


def single(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {
        'product': product
    }
    return render(request, 'user/shop/single_page.html', context)
    


      