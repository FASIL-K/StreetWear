from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from cart.models import Cart
from products.models import Product,Size
from django.http.response import JsonResponse
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User

# Create your views here.

def get_or_create_anonymous_user():
    anonymous_user, created = User.objects.get_or_create(username='anonymous_user')
    return anonymous_user

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cart(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = get_or_create_anonymous_user()

    cart = Cart.objects.filter(user_id=user.id).order_by('id')
    
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

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addtocart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('prod_id'))
        product_check = Product.objects.get(id=prod_id)
            
        if product_check:
            prod_qty = int(request.POST.get('product_qty'))
            selected_size = int(request.POST.get('size'))  # Get the selected size from the POST data

            if request.user.is_authenticated:
                user = request.user
            else:
                user = get_or_create_anonymous_user()

            # Check if the same product with the same size already exists in the cart
            cart_item = Cart.objects.filter(user_id=user.id, product_id=prod_id, selected_size=selected_size).first()

            if cart_item:
                return JsonResponse({'status': "Product Already in Cart"})
            else:
                # If the product with the selected size is not in the cart, create a new cart item
                if product_check.stock >= prod_qty:
                    Cart.objects.create(
                        user_id=user.id,
                        product_id=prod_id,
                        product_qty=prod_qty,
                        selected_size=selected_size,
                    )
                    return JsonResponse({'status': "Product added successfully"})
                else:
                    return JsonResponse({'status': "Only " + str(product_check.stock) + " quantity available"})
        else:
            return JsonResponse({'status': "No such product found"})

# Update cart quantity
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        selected_size = request.POST.get('selected_size')
        cart_id = request.POST.get('cart_id')
        
        
        if (Cart.objects.get(id=cart_id)):

            prod_qty = request.POST.get('product_qty')
            cart = Cart.objects.get(id=cart_id)
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
# @login_required(login_url='signin')
def deletecartitem(request, id):
    cart_id = request.POST.get(id)
    cart_items = Cart.objects.filter(id=id)
    if cart_items.exists():
        cart_items.delete()
    return redirect('cart')

def update_cart_item_size(request):
    if request.method == 'POST':
        cart_id = request.POST.get('cartid')
        selected_size = request.POST.get('size')
        if cart_id:
            cart_item = Cart.objects.get(id=cart_id)
            cart_item.selected_size = selected_size
            cart_item.save()
            size = Size.objects.get(id=cart_item.selected_size)
            return JsonResponse({'status': 'Size updated successfully','sizename':size.name})
        else:
            return JsonResponse({'status': 'Cart item not found'}, status=404)
    else:
        return JsonResponse({'status': 'Invalid request method'}, status=400)