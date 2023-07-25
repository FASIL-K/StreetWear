from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from cart.models import Cart
from products.models import Product,Size
from django.http.response import JsonResponse
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


# Create your views here.



def cart(request):
    cart = Cart.objects.filter(user=request.user).order_by('id')
    
    # Fetch size names based on the IDs in the cart items
    for item in cart:
        try:
            item.selected_size = Size.objects.get(id=item.selected_size).name
        except Size.DoesNotExist:
            item.selected_size = "Unknown Size"  # Handle the case where the size ID does not exist in the Size model
        
    total_price = sum(item.product.product_price * item.product_qty for item in cart)
    tax = total_price * 0.18
    grand_total = total_price + tax

    context = {
        'cart': cart,
        'total_price': total_price,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'user/cart/cart.html', context)

def addtocart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('prod_id'))
            product_check = Product.objects.get(id=prod_id)
            if product_check:
                if Cart.objects.filter(user=request.user.id, product_id=prod_id):
                    return JsonResponse({'status': "Product Already in Cart"})
                else:
                    prod_qty = int(request.POST.get('product_qty'))
                    selected_size = int(request.POST.get('size')) # Get the selected size from the POST data

                    if product_check.stock >= prod_qty:
                        # Save the cart item with the selected size
                        Cart.objects.create(
                            user=request.user,
                            product_id=prod_id,
                            product_qty=prod_qty,
                            selected_size=selected_size,
                        )
                        return JsonResponse({'status': "Product added successfully"})
                    else:
                        return JsonResponse({'status': "Only " + str(product_check.stock) + " quantity available"})
            else:
                return JsonResponse({'status': "No such product found"})
        else:
            return JsonResponse({'status': "Login to Continue"})

    return redirect('addtocart')
# Update cart quantity
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if (Cart.objects.filter(user=request.user, product_id=product_id)):
            prod_qty = request.POST.get('product_qty')
            cart = Cart.objects.get(product_id=product_id, user=request.user)
            cartes = cart.product.stock
            if int(cartes) >= int(prod_qty):
                cart.product_qty = prod_qty
                cart.save()

                carts = Cart.objects.filter(user=request.user).order_by('id')
                total_price = sum(item.product.product_price * item.product_qty for item in carts)
                tax = total_price * 0.18
                grand_total = total_price + tax

                return JsonResponse({
                    'status': 'Updated successfully',
                    'sub_total': total_price,
                    'tax': tax,
                    'grand_total': grand_total,
                    'product_price': cart.product.product_price,
                    'quantity': prod_qty
                })
            else:
                return JsonResponse({'status': 'Not allowed this Quantity'})
    return HttpResponse('Something went wrong, reload page')


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def deletecartitem(request,product_id):
    
    
    product_id = product_id
    cart_items = Cart.objects.filter(user=request.user, product=product_id)
    if cart_items.exists():
        cart_items.delete()
    return redirect('cart')

